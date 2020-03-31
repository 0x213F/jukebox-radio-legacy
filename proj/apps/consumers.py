import asyncio
import requests_async
from cryptography.fernet import Fernet
from datetime import datetime
from datetime import timedelta
import json
import uuid
from urllib import parse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.serializers import serialize

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from urllib.parse import urlparse


from proj.apps.music.models import Ticket
from proj.apps.music.models import Comment
from proj.apps.users.models import Profile
from proj.apps.music.models import Stream
from proj.apps.music.models import Record
from proj.apps.music.models import TrackListing
from proj.core.resources import Spotify


class Consumer(AsyncConsumer):

    # - - - -
    # constants
    # - - - -

    PLAY_BAR_AUTHORIZE_SPOITFY = 'authorize-spotify'

    ACTION_COMMENT = 'comment'

    # - - - -
    # helpers
    # - - - -

    def get_data_from_ws_path(self):
        '''
        Takes a path from the query_string and parses it into a dict
        '''
        ws_path = self.scope['query_string']
        return dict(
            parse.parse_qsl(parse.urlsplit(ws_path).path.decode("utf-8"))
        )

    # - - - -
    # connect
    # - - - -

    async def websocket_connect(self, event):

        # accept connection
        await self.websocket_accept()

        # parse data from WSS URL
        url_params = self.get_data_from_ws_path()
        stream_uuid = url_params['uuid']

        # get user's profile
        self.scope['profile'] = await database_sync_to_async(
            Profile.objects.get
        )(user=self.scope['user'])

        # init spotify interface
        self.scope['spotify'] = Spotify(
            self.scope['user'], profile=self.scope['profile']
        )

        # join stream, grab stuff from DB
        self.scope['stream'], self.scope['ticket'], self.scope['profile'] = await Profile.objects.join_stream_async(
            self.scope['user'], stream_uuid,
        )

        # add to channel
        await self.add_to_channel()
        user_id = self.scope['user'].id
        await self.channel_layer.group_add(f'user-{user_id}', self.channel_name)

        # send back recent chat activity
        should_display_comments = url_params['display_comments'] == 'true'
        if should_display_comments:
            comments_qs = Comment.objects.select_related('commenter_ticket').recent(self.scope['stream'])
            comments = await database_sync_to_async(list)(comments_qs)
            await self.send_comments(comments)

        # verify the user has an active spotify token
        try:
            await self.scope['spotify'].get_user_info_async()
        except requests_async.exceptions.HTTPError:
            await self.update_playbar(self.PLAY_BAR_AUTHORIZE_SPOITFY)
            return

        # sync playback
        await self.sync_playback(onload=True)

    # - - - - -
    # receieve
    # - - - - -

    async def websocket_receive(self, event):
        payload = json.loads(event["text"])
        # action = payload['action']

        if 'resync' in payload:
            await self.sync_playback()
            return

        # create comment in DB
        # if action == self.ACTION_COMMENT:
        comment = await (
            Comment.objects.create_from_payload_async(
                self.scope["user"], payload,
                stream=self.scope["stream"], ticket=self.scope["ticket"]
            )
        )
        await self.channel_post_comment(comment)

        # if action == self.ACTION_DISCONNECT:
        #     pass

    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):

        _user = self.scope["user"]
        await Profile.objects.leave_stream_async(self.scope['user'])

        ticket = self.scope['ticket']

        ticket.is_active = False
        await database_sync_to_async(Ticket.objects.filter(id=ticket.id).update)(is_active=False)

        await self.remove_from_channel()
        user_id = self.scope['user'].id
        await self.channel_layer.group_discard(
            f'user-{user_id}', self.channel_name
        )

        # Create record of comment.
        payload = {
            "stream_uuid": self.scope['stream'].uuid,
            "status": Comment.STATUS_LEFT,
            "text": None,
        }
        comment = await (
            Comment.objects.create_from_payload_async(self.scope['user'], payload, stream=self.scope['stream'], ticket=self.scope['ticket'])
        )

        await self.channel_layer.group_send(  # TODO: put as manager method
            self.scope['stream'].chat_room,
            {
                "type": "broadcast",
                "text": json.dumps(
                    {
                        "data": {
                            "comments": [Comment.objects.serialize(comment, ticket=ticket)]
                        }
                    }
                ),
            },
        )

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def broadcast(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})
        try:
            if bool(event["playback"]) and bool(self.scope['spotify'].token):
                await self.play_tracks(event["playback"])
        except:
            pass

    async def play_tracks(self, playback):
        token = self.scope['spotify'].token
        action = playback["action"]
        data = json.dumps(playback["data"]) or {}
        response = await requests_async.put(
            f"https://api.spotify.com/v1/me/player/{action}",
            data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

    async def promote_to_host(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "promote_to_host": True,
                    }
                }),
            }
        )

    async def demote_from_host(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "promote_to_host": False,
                    }
                }),
            }
        )

    async def update_queue(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "update_queue": True,
                    }
                }),
            }
        )

    async def update_name(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})

    # - - - - - - - - - - - - - -
    #          HELPERS           |
    # - - - - - - - - - - - - - -

    async def websocket_accept(self):
        await self.send({"type": "websocket.accept"})

    async def add_to_channel(self):
        await (
            self.channel_layer.group_add(self.scope['stream'].chat_room, self.channel_name)
        )

        # create db log
        join_payload = {
            "stream_uuid": self.scope['stream'].uuid,
            "status": Comment.STATUS_JOINED,
            "text": None,
        }
        comment = await (
            Comment.objects.create_from_payload_async(
                self.scope['user'], join_payload, stream=self.scope['stream'], ticket=self.scope['ticket'],
            )
        )

        await self.channel_post_comment(comment)

    async def remove_from_channel(self):
        await self.channel_layer.group_discard(
            self.scope['stream'].chat_room, self.channel_name
        )

    async def channel_post_comment(self, comment):
        await self.channel_layer.group_send(
            self.scope['stream'].chat_room,
            {
                "type": "broadcast",
                "text": json.dumps({
                    "data": {
                        "comments": [
                            Comment.objects.serialize(
                                comment, ticket=self.scope['ticket']
                            )
                        ],
                        "playback": {
                            'next_step': 'noop',
                        }
                    }
                }),
            },
        )

    async def update_playbar(self, status):
        stream = Stream.objects.serialize(self.scope['stream'])
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "stream": stream,
                        "playback": {
                            "next_step": status,
                        }
                    }
                }),
            }
        )

    async def send_comments(self, comments):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "comments": [
                            Comment.objects.serialize(c, ticket=c.commenter_ticket)
                            for c in comments
                        ],
                        "playback": {
                            'next_step': 'noop',
                        }
                    }
                }),
            }
        )

    async def send_record(self, record):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "record": Record.objects.serialize(record),
                        "playback": {
                            "next_step": 'currently-playing',
                        }
                    }
                }),
            }
        )

    #############################

    async def sync_playback(self, onload=False):
        self.scope['stream'] = await database_sync_to_async(
            Stream.objects.select_related('current_record').get
        )(id=self.scope['stream'].id)

        record_terminates_at = self.scope['stream'].record_terminates_at
        if (
            record_terminates_at and
            datetime.now() > record_terminates_at.replace(tzinfo=None)
        ):
            await self.update_playbar('waiting-for-stream-to-start')
            return

        # [6]
        # get the now playing target progress in ms
        try:
            now_playing = await database_sync_to_async(
                Comment.objects.select_related('track', 'record')
                .filter(
                    created_at__lte=datetime.now(),
                    stream__uuid=self.scope['stream'].uuid,
                    status=Comment.STATUS_START,
                )
                .order_by("-created_at")
                .first
            )()
            assert now_playing
        except Exception as e:
            await self.update_playbar('waiting-for-stream-to-start')
            return

        # [7]
        # determine if the user's Spotify is already synced with the stream
        try:
            currently_playing_data = await (
                self.scope['spotify'].get_currently_playing_async()
            )

            spotify_track_duration_ms = currently_playing_data['spotify_ms']
            spotify_uri = currently_playing_data['spotify_uri']
            spotify_is_playing = currently_playing_data['spotify_is_playing']

            ms_since_track_was_played = (
                datetime.now() - now_playing.created_at.replace(tzinfo=None)
            ).total_seconds() * 1000
            offsync_ms = abs(
                ms_since_track_was_played - spotify_track_duration_ms
            )

            user_is_already_in_sync = (
                spotify_is_playing
                and spotify_uri == now_playing.track.spotify_uri
                and offsync_ms < 5000
            )

            if user_is_already_in_sync:
                record = now_playing.record
                if onload:
                    await self.send_record(record)
                return

        except Exception as e:
            # assuming everything is behaving as expected, we assume that the
            # user's Spotify client is disconnected
            await self.update_playbar(
                'spotify-streaming-client-not-found'
            )
            return

        # [8]
        # get the track playing and tracks in the queue
        uris = (
            self.scope['stream'].current_record.tracks_through
            .order_by('number').values_list('track__spotify_uri', flat=True)
        )
        uris = await database_sync_to_async(list)(uris)
        while uris:  # TODO: BUG!
            if uris[0] == now_playing.track.spotify_uri:
                break
            uris = uris[1:]

        if not uris:
            return

        # [9]
        # sync the user's playback with the stream
        ms_since_track_was_played = (
            datetime.now() - now_playing.created_at.replace(tzinfo=None)
        ).total_seconds() * 1000
        await self.play_tracks(
            {
                "action": "play",
                "data": {
                    "uris": uris,
                    "position_ms": ms_since_track_was_played,
                },
            }
        )

        # [A]
        # update the front-end with playback status
        record = now_playing.record
        await self.send_record(record)
