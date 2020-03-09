import asyncio
from cryptography.fernet import Fernet
from datetime import datetime
from datetime import timedelta
import json
import requests
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
from proj.core.resources.cache import _get_or_fetch_from_cache
from proj.core.fns import results


class Consumer(AsyncConsumer):

    # - - - -
    # helpers
    # - - - -

    def initialize_cache(self):
        '''
        We attach any expensive data (typically from the DB) to the instance
        '''
        self._cache = {}

    async def get_user(self):
        '''
        Gets the instance's users along with their profile
        '''
        try:
            self._cache['profile']
        except KeyError:
            self._cache['profile'] = await database_sync_to_async(
                Profile.objects.get
            )(user=self.scope['user'])
            self.scope['user'].profile = self._cache['profile']
        finally:
            return self.scope['user']

    @property
    def spotify(self):
        try:
            return self._spotify
        except AttributeError:
            self._spotify = Spotify(self.scope['user'])
            return self._spotify

    def get_spotify(self):
        return Spotify(self.scope['user'])

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
        self.initialize_cache()
        _user = await self.get_user()

        # [0]
        # user needs to have Spotify linked before joining the stream/ channel
        if not _user.profile.spotify_access_token:
            await self.send_playback_status('linkspotify')
            return

        url_params = self.get_data_from_ws_path()
        active_stream_uuid = url_params['uuid']

        await Profile.objects.join_stream_async(
            _user, active_stream_uuid, _cache=self._cache,
        )

        await self.add_to_channel()

        await self.websocket_accept()

        # [1]
        # create record of joining
        join_payload = {
            "stream_uuid": active_stream_uuid,
            "status": Comment.STATUS_JOINED,
            "text": None,
        }
        comment = await (
            Comment.objects.create_from_payload_async(
                _user, join_payload, stream=self._cache['stream'], ticket=self._cache['ticket'],
            )
        )
        self._cache['comment'] = comment

        # [2]
        # tell the chatroom that the user has joined
        await self.channel_post_comment(
            self._cache['stream'],
            self._cache['comment'],
            self._cache['ticket'],
        )

        # [3]
        # get comments from the last 30 min
        comments_qs = Comment.objects.recent(active_stream_uuid)
        comments = await database_sync_to_async(list)(comments_qs)

        # [4]
        # send comments just to the current user
        await self.send_comments(comments)

        # [5]
        # if no record is currently playing, return
        record_ends_at = (
            self._cache['stream']
            .record_terminates_at.replace(tzinfo=None)
        )
        if datetime.now() > record_ends_at:
            await self.send_playback_status('waiting')
            return

        # [6]
        # get the now playing target progress in ms
        try:
            now_playing = await database_sync_to_async(
                Comment.objects.select_related('track', 'record')
                .filter(
                    created_at__lte=datetime.now(),
                    stream__uuid=active_stream_uuid,
                    status=Comment.STATUS_START,
                )
                .order_by("-created_at")
                .first
            )()
            assert now_playing
        except Exception as e:
            await self.send_playback_status('waiting')
            return

        # [7]
        # determine if the user's Spotify is already synced with the stream
        try:
            currently_playing_data = await (
                self.spotify.get_currently_playing_async()
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
                await self.send_record(record)
                return

        except Exception as e:
            # assuming everything is behaving as expected, we assume that the
            # user's Spotify client is disconnected
            await self.send_playback_status('disconnected')
            return

        # [8]
        # get the track playing and tracks in the queue
        uris = (
            self._cache['stream'].current_record.tracks_through
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
            self.spotify.token,
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

    # - - - - -
    # receieve
    # - - - - -

    async def websocket_receive(self, event):
        payload = json.loads(event["text"])

        # create comment in DB
        comment = await (
            Comment.objects.create_from_payload_async(
                self.scope["user"], payload,
                stream=self._cache['stream'], ticket=self._cache['ticket']
            )
        )

        await self.channel_post_comment(self._cache['stream'], comment, self._cache['ticket'])

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def broadcast(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})

        try:
            if bool(event["playback"]) and bool(self.spotify.token):
                await self.play_tracks(self.spotify.token, event["playback"])
        except:
            pass

    async def play_tracks(self, sat, playback):
        action = playback["action"]
        data = json.dumps(playback["data"]) or {}
        response = requests.put(
            f"https://api.spotify.com/v1/me/player/{action}",
            data=data,
            headers={
                "Authorization": f"Bearer {sat}",
                "Content-Type": "application/json",
            },
        )

    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):

        _user = self.scope["user"]
        await Profile.objects.leave_stream_async(_user)

        url_params = self.get_data_from_ws_path()
        active_stream_uuid = url_params['uuid']

        stream = self._cache["stream"]

        ticket = await database_sync_to_async(Ticket.objects.get)(
            holder=_user, stream=stream,
        )

        await self.remove_from_channel()

        # Create record of comment.
        payload = {
            "stream_uuid": active_stream_uuid,
            "status": Comment.STATUS_LEFT,
            "text": None,
        }
        comment = await (
            Comment.objects.create_from_payload_async(_user, payload, stream=self._cache['stream'], ticket=self._cache['ticket'],)
        )
        self._cache['comment'] = comment

        await self.channel_layer.group_send(  # TODO: put as manager method
            self._cache["stream"].chat_room,
            {
                "type": "broadcast",
                "text": json.dumps(
                    {
                        "data": {
                            "comments": [Comment.objects.serialize(self._cache["comment"], ticket=ticket)]
                        }
                    }
                ),
            },
        )

    # - - - - - - - - - - - - - -
    #          HELPERS           |
    # - - - - - - - - - - - - - -

    async def websocket_accept(self):
        await self.send({"type": "websocket.accept"})

    async def add_to_channel(self):
        self._channel_name = self._cache['stream'].chat_room
        await (
            self.channel_layer.group_add(self._channel_name, self.channel_name)
        )

    async def remove_from_channel(self):
        assert self._channel_name
        await self.channel_layer.group_discard(
            self._channel_name, self.channel_name
        )
        self._channel_name = None

    async def channel_post_comment(self, stream, comment, ticket):
        await self.channel_layer.group_send(
            stream.chat_room,
            {
                "type": "broadcast",
                "text": json.dumps({
                    "data": {
                        "comments": [
                            Comment.objects.serialize(
                                comment, ticket=ticket
                            )
                        ],
                    }
                }),
            },
        )

    async def send_playback_status(self, status):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "stream": {
                            **Stream.objects.serialize(self._cache["stream"])
                        },
                        "playback": {
                            "status": status,
                        }
                    }
                }),
            }
        )

    async def send_comments(self, comments, ticket=None):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "comments": [
                            Comment.objects.serialize(c, ticket=ticket)
                            for c in comments
                        ],
                    }
                }),
            }
        )

    async def send_record(self, record):
        qs = TrackListing.objects.select_related('track').filter(record=record)
        tracklistings = await database_sync_to_async(list)(qs)

        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "record": Record.objects.serialize(record),
                        "tracklistings": [
                            TrackListing.objects.serialize(tracklisting)
                            for tracklisting in tracklistings
                        ],
                        "playback": {
                            "status": 'play_record',
                        }
                    }
                }),
            }
        )
