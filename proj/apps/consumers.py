import json
from datetime import datetime
from urllib import parse

import requests_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from proj.apps.music.models import (Comment, Queue, QueueListing, Record,
                                    Stream, Ticket, Track)
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

    async def _websocket_receive_bytes(self, bytes):
        await self.channel_layer.group_send(
            self.scope["stream"].chat_room, {"type": "send_audio", "bytes": bytes,}
        )

    async def _websocket_receive_data(self, data):
        await Comment.objects.create_and_share_comment_async(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            text=data["text"],
        )

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

    async def sync_playback(self):

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
