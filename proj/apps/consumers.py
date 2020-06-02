import json
import wave
from datetime import datetime
from urllib import parse

from django.core.cache import cache

import requests_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import io

from proj.apps.music.models import (
    Comment,
    Queue,
    QueueListing,
    Record,
    Stream,
    Ticket,
    Track,
)
from proj.apps.users.models import Profile
from proj.core.resources import Spotify


class Consumer(AsyncConsumer):

    # - - - -
    # constants
    # - - - -

    PLAY_BAR_AUTHORIZE_SPOITFY = "authorize-spotify"

    # - - - -
    # helpers
    # - - - -

    def get_data_from_ws_path(self):
        """
        Takes a path from the query_string and parses it into a dict
        """
        ws_path = self.scope["query_string"]
        return dict(parse.parse_qsl(parse.urlsplit(ws_path).path.decode("utf-8")))

    # - - - -
    # connect
    # - - - -

    async def websocket_connect(self, event):

        # accept connection
        await self.websocket_accept()

        # parse data from WSS URL
        url_params = self.get_data_from_ws_path()
        stream_uuid = url_params["uuid"]

        # get user's profile
        self.scope["profile"] = await database_sync_to_async(Profile.objects.get)(
            user=self.scope["user"]
        )

        # init spotify interface
        self.scope["spotify"] = Spotify(
            self.scope["user"], profile=self.scope["profile"]
        )

        # join stream, grab stuff from DB
        (
            self.scope["stream"],
            self.scope["ticket"],
            self.scope["profile"],
        ) = await Profile.objects.join_stream_async(self.scope["user"], stream_uuid)

        # say who the current hosts are
        ticket_qs = Ticket.objects.administrators(self.scope["stream"])
        tickets = await database_sync_to_async(list)(ticket_qs)

        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {
                        "read": {
                            "tickets": [
                                Ticket.objects.serialize(ticket) for ticket in tickets
                            ],
                        }
                    }
                ),
            }
        )

        # add to channel
        await self.add_to_channel()

        await self.send_update(
            {"read": {"streams": [Stream.objects.serialize(self.scope["stream"])]}}
        )

        # send back recent chat activity
        comments_qs = Comment.objects.select_related("commenter_ticket").recent(
            self.scope["stream"]
        )
        comments = await database_sync_to_async(list)(comments_qs)
        await self.send_update(
            {"read": {"comments": [Comment.objects.serialize(c) for c in comments]}}
        )

        # create db log
        await Comment.objects.create_and_share_comment_async(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            status=Comment.STATUS_JOINED,
        )

        # send playback status
        await self.sync_playback()

    # - - - - -
    # receieve
    # - - - - -

    async def websocket_receive(self, event):
        if "bytes" in event:
            bytes = event["bytes"]
            await self._websocket_receive_bytes(bytes)
        elif "text" in event:
            data = json.loads(event["text"])
            await self._websocket_receive_data(data)

    async def _websocket_receive_bytes(self, byte_data):
        ticket = self.scope["ticket"]

        if "microphone" not in self.scope:
            self.scope["microphone"] = bytearray()
            ticket.is_speaking = True

        self.scope["microphone"].extend(byte_data)

        INITIALIZATION_SEGMENT_LENGTH = 161

        microphone_len = len(self.scope["microphone"])

        if microphone_len >= INITIALIZATION_SEGMENT_LENGTH:
            initialization_segment = self.scope["microphone"][
                :INITIALIZATION_SEGMENT_LENGTH
            ]
            if ticket.initialization_segment != initialization_segment:
                ticket.initialization_segment = initialization_segment

        if ticket.initialization_segment:
            if "_partial_block_idx" not in self.scope:
                self.scope["_partial_block_idx"] = INITIALIZATION_SEGMENT_LENGTH

            partial_block_idx = self.scope["_partial_block_idx"]

            while True:
                block_size_raw = self.scope["microphone"][
                    partial_block_idx + 1 : partial_block_idx + 3
                ]
                block_size = (
                    int.from_bytes(block_size_raw, byteorder="big", signed=False) + 3
                )
                block_size = block_size & 0x0FFF

                if partial_block_idx + block_size > microphone_len:
                    ticket.partial_block = self.scope["microphone"][partial_block_idx:]
                    break

                partial_block_idx += block_size
                self.scope["_partial_block_idx"] = partial_block_idx

        await database_sync_to_async(ticket.save)()

        await self.channel_layer.group_send(
            self.scope["stream"].chat_room, {"type": "send_audio", "bytes": byte_data,}
        )

    async def _websocket_receive_data(self, data):
        if "text" in data:
            await Comment.objects.create_and_share_comment_async(
                self.scope["user"],
                self.scope["stream"],
                self.scope["ticket"],
                text=data["text"],
            )

        if "transcript" in data:
            data["holder_uuid"] = str(self.scope["ticket"].uuid)

            await self.channel_layer.group_send(
                self.scope["stream"].chat_room,
                {"type": "send_update", "text": {"updated": {"transcripts": [data]}},},
            )

        if "connect_to_livestream" in data:

            # init audio playback if there is a livestream happening
            speaker = await database_sync_to_async(
                self.scope["stream"].tickets.filter(is_speaking=True).first
            )()
            if speaker:
                initial_audio_bytes = bytearray()
                initial_audio_bytes.extend(speaker.initialization_segment)
                initial_audio_bytes.extend(speaker.partial_block)
                await self.send(
                    {"type": "websocket.send", "bytes": bytes(initial_audio_bytes),}
                )

            self.scope["is_tuned_in_to_livestream"] = True

    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):

        # remove from group channel
        await self.channel_layer.group_discard(
            self.scope["stream"].chat_room, self.channel_name
        )

        # create DB record
        await Profile.objects.leave_stream_async(
            self.scope["user"], self.scope["ticket"], self.scope["stream"]
        )

        # remove from group channel
        await self.channel_layer.group_discard(
            self.scope["stream"].chat_room, self.channel_name
        )

        # remove from individual channel
        user_id = self.scope["user"].id
        await self.channel_layer.group_discard(f"user-{user_id}", self.channel_name)

        # create db log
        await Comment.objects.create_and_share_comment_async(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            status=Comment.STATUS_LEFT,
        )

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def send_update(self, data):
        if set(["type", "text"]) == set(data.keys()):
            data = data["text"]
        await self.send(
            {"type": "websocket.send", "text": json.dumps(data),}
        )

    async def send_audio(self, event):
        if not self.scope["is_tuned_in_to_livestream"]:
            return
        await self.send(
            {"type": "websocket.send", "bytes": event["bytes"],}
        )

    async def play_tracks(self, playback):
        token = self.scope["spotify"].token
        action = playback["action"]
        data = json.dumps(playback["data"]) or {}
        await requests_async.put(
            f"https://api.spotify.com/v1/me/player/{action}",
            data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

    # - - - - - - - - - - - -
    # helpers
    # - - - - - - - - - - - -

    async def websocket_accept(self):
        await self.send({"type": "websocket.accept"})

    async def add_to_channel(self):
        # add to group channel
        await self.channel_layer.group_add(
            self.scope["stream"].chat_room, self.channel_name
        )

        # add to individual channel
        user_id = self.scope["user"].id
        await self.channel_layer.group_add(f"user-{user_id}", self.channel_name)

    # - - - - - - - - - - - -
    # helpers
    # - - - - - - - - - - - -

    async def sync_playback(self, event=None):

        # get user's profile to refresh spotify token
        self.scope["profile"] = await database_sync_to_async(Profile.objects.get)(
            user=self.scope["user"]
        )

        # init spotify interface
        self.scope["spotify"] = Spotify(
            self.scope["user"], profile=self.scope["profile"]
        )

        # reload stream object
        self.scope["stream"] = await database_sync_to_async(
            Stream.objects.select_related(
                "current_queue",
                "current_queue__record",
                "current_tracklisting",
                "current_tracklisting__track",
            ).get
        )(id=self.scope["stream"].id)

        # nothing is happening, come back later
        record_terminates_at = self.scope["stream"].record_terminates_at
        if not record_terminates_at:
            playback_data = {
                "record": None,
                "queuelistings": None,
                "stream": Stream.objects.serialize(self.scope["stream"]),
                "status": "waiting-for-stream-to-start",
                "spotify_token": self.scope["spotify"].token,
                "ticket": Ticket.objects.serialize(self.scope["ticket"]),
            }
            payload = {
                "read": {"playback": [playback_data]},
            }
            await self.send_update(payload)
            return

        # base case: first spin
        current_queue = self.scope["stream"].current_queue
        record = current_queue.record

        queue_qs = Queue.objects.select_related("stream", "record").in_stream(
            self.scope["stream"]
        )
        queues = await database_sync_to_async(list)(queue_qs)

        if record.spotify_uri:
            current_queue_listing = await QueueListing.objects.select_related(
                "track_listing", "track_listing__track"
            ).now_playing_async(current_queue)
            up_next_qls = await QueueListing.objects.select_related(
                "track_listing", "track_listing__track"
            ).up_next_async(current_queue)
            qls = [QueueListing.objects.serialize(current_queue_listing)]
            qls.extend([QueueListing.objects.serialize(ql) for ql in up_next_qls])

            playback_data = {
                "record": Record.objects.serialize(record),
                "queuelistings": qls,
                "stream": Stream.objects.serialize(self.scope["stream"]),
                "status": "playing_and_synced",
                "spotify_token": self.scope["spotify"].token,
                "ticket": Ticket.objects.serialize(self.scope["ticket"]),
                "up_next": [Queue.objects.serialize(q) for q in queues],
            }
        else:
            playback_data = {
                "record": Record.objects.serialize(record),
                "queuelistings": [],
                "stream": Stream.objects.serialize(self.scope["stream"]),
                "status": "playing_and_synced",
                "spotify_token": self.scope["spotify"].token,
                "ticket": Ticket.objects.serialize(self.scope["ticket"]),
                "up_next": [Queue.objects.serialize(q) for q in queues],
            }

        payload = {
            "read": {"playback": [playback_data]},
        }
        await self.send_update(payload)
