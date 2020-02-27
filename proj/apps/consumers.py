import asyncio
from cryptography.fernet import Fernet
from datetime import datetime
from datetime import timedelta
import json
import requests
import uuid

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
from proj.core.resources.cache import _get_or_fetch_from_cache
from proj.core.fns import results


class Consumer(AsyncConsumer):

    # - - - -
    # connect
    # - - - -

    async def websocket_connect(self, event):
        """
        """
        _cache = {}
        _user = self.scope["user"]

        cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)

        active_stream_uuid = self.scope["query_string"][5:].decode("utf-8")
        _cache = await Profile.objects.join_stream_async(
            _user, active_stream_uuid, _cache=_cache,
        )
        _user_profile = _cache["profile"]
        ticket = _cache["ticket"]

        channel_name = _cache["stream"].chat_room
        await self.add_to_channel(channel_name)

        await self.websocket_accept()


        # if ticket:
        #     await self.send(
        #         {
        #             "type": "websocket.send",
        #             "text": json.dumps(
        #                 {"data": {"ticket": Ticket.objects.serialize(ticket),}}
        #             ),
        #         }
        #     )

        if not _user_profile.spotify_access_token:
            await self.send_stream_status(
                active_stream_uuid,
                'linkspotify'
            )
            return

        # Create record of comment.
        join_payload = {
            "stream_uuid": active_stream_uuid,
            "status": Comment.STATUS_JOINED,
            "text": None,
        }
        _cache = await (
            Comment.objects.create_from_payload_async(
                _user, join_payload, _cache=_cache
            )
        )
        comment = _cache["comment"]

        # tell the chatroom that the user has joined
        stream = _cache["stream"]
        join_comment = _cache["comment"]
        await self.channel_post_comment(stream, join_comment, ticket)

        # get comments from the last 30 min
        now = datetime.now()
        comments_qs = (
            Comment.objects
            .select_related('commenter_ticket')
            .filter(
                created_at__gte=now - timedelta(minutes=30),
                stream__uuid=active_stream_uuid,
            )
            .order_by('created_at')
        )
        comments = await database_sync_to_async(
            list
        )(comments_qs)

        # send comments just to the current user
        await self.send_comments(comments)

        # get active record, if it exists
        # now = datetime.now()
        try:
            stream = await database_sync_to_async(
                Stream.objects.select_related("current_record").get
            )(
                uuid=active_stream_uuid,
                status=Stream.STATUS_ACTIVATED,
                current_record__isnull=False,
                record_terminates_at__gt=(now + timedelta(seconds=5)),
            )
        except Exception as e:
            await self.send_stream_status(active_stream_uuid, 'waiting')
            return

        # get the now playing target progress in ms
        try:
            now_playing = await database_sync_to_async(
                Comment.objects.select_related('track', 'record')
                .filter(
                    created_at__lte=now,
                    stream__uuid=active_stream_uuid,
                    status=Comment.STATUS_START,
                )
                .order_by("-created_at")
                .first
            )()

        except Exception as e:
            await self.send_stream_status(active_stream_uuid, 'waiting')
            return

        assert now_playing

        expected_ms = (
            now_playing.created_at.replace(tzinfo=None) - now
        ).total_seconds() * 1000

        # get the actual progress in ms
        try:
            user_spotify_access_token = cipher_suite.decrypt(
                _user_profile.spotify_access_token.encode("utf-8")
            ).decode("utf-8")
            response = requests.get(
                "https://api.spotify.com/v1/me/player/currently-playing",
                headers={
                    "Authorization": f"Bearer {user_spotify_access_token}",
                    "Content-Type": "application/json",
                },
            )

            response_json = response.json()

            spotify_ms = response_json["progress_ms"]
            spotify_uri = response_json["item"]["uri"]
            spotify_is_playing = response_json["is_playing"]

            track_is_already_playing = (
                spotify_is_playing
                and spotify_uri == now_playing.track.spotify_uri
                and abs(expected_ms + spotify_ms) < 5000
            )

            record_is_over = False  # abs(spotify_ms + expected_ms) > 5000
            if track_is_already_playing or record_is_over:
                # the user is already tuned into this stream
                record = now_playing.record
                await self.send_record(record)
                return

        except Exception as e:
            try:
                # edge case that is only hit when one of the following happens:
                # - user revokes our app from their settings page then comes
                #   back again to use the site
                # - cron messes up and we don't refresh tokens so they all
                #   expire
                if response.status_code == 204:
                    raise Exception('The user does not have Spotify open')
                if response_json['error']['message'] == 'The access token expired':
                    await self.send_stream_status(
                        active_stream_uuid,
                        'linkspotify'
                    )
                else:
                    raise Exception()
            except Exception:
                await self.send_stream_status(active_stream_uuid, 'disconnected')
            finally:
                return

        # get other tracks to play in future
        uris = stream.current_record.tracks_through.order_by("number").values_list(
            "track__spotify_uri", flat=True
        )
        uris = await database_sync_to_async(list)(uris)
        while uris:
            if uris[0] == now_playing.track.spotify_uri:
                break
            uris = uris[1:]

        if not uris:
            return

        await self.play_tracks(
            user_spotify_access_token,
            {"action": "play", "data": {"uris": uris, "position_ms": -expected_ms},},
        )

        record = now_playing.record
        await self.send_record(record)

    # - - - - -
    # receieve
    # - - - - -

    async def websocket_receive(self, event):
        payload = json.loads(event["text"])
        _user = self.scope["user"]
        _cache = {}

        # Validate request payload.
        is_valid, _cache = await (
            Comment.objects.validate_create_comment_payload_async(_user, payload)
        )
        if is_valid == results.RESULT_FAILED_VALIDATION:
            return
        elif is_valid == results.RESULT_PERFORM_SIDE_EFFECT_ONLY:
            # Display initial chat content.
            comments = await Comment.objects.list_comments_async(
                _cache["stream"], payload["most_recent_comment_timestamp"]
            )
            comments = [Comment.objects.serialize(comment) for comment in comments]
            await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps({"data": {"comments": comments}}),
                }
            )
            return

        # Create record of comment.
        _cache = await (
            Comment.objects.create_from_payload_async(_user, payload, _cache=_cache)
        )

        stream = await database_sync_to_async(Stream.objects.get)(
            uuid=payload["stream_uuid"]
        )
        _cache["stream"] = stream

        ticket = await database_sync_to_async(Ticket.objects.get)(
            holder=_user, stream=_cache["stream"],
        )

        comment = _cache["comment"]
        await self.channel_post_comment(stream, comment, ticket)

        if payload["status"] == Comment.STATUS_LEFT:
            # If leaving the chat, send final comment response back to original
            # user.
            comments = [_cache["comment"]]
            await self.send_comments(comments)
            return

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def broadcast(self, event):
        """
        """
        _user = self.scope["user"]

        await self.send(
            {"type": "websocket.send", "text": event["text"],}
        )

        _profile = await database_sync_to_async(Profile.objects.get)(user=_user)

        cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)
        user_spotify_access_token = cipher_suite.decrypt(
            _profile.spotify_access_token.encode("utf-8")
        ).decode("utf-8")
        try:
            if bool(event["playback"]) and bool(user_spotify_access_token):
                await self.play_tracks(user_spotify_access_token, event["playback"])
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
        _cache = {}
        _user = self.scope["user"]
        await Profile.objects.leave_stream_async(_user)
        active_stream_uuid = self.scope["query_string"][5:].decode("utf-8")
        stream = await database_sync_to_async(Stream.objects.get)(
            uuid=active_stream_uuid
        )
        _cache["stream"] = stream

        ticket = await database_sync_to_async(Ticket.objects.get)(
            holder=_user, stream=stream,
        )

        await (
            self.channel_layer.group_discard(
                _cache["stream"].chat_room, self.channel_name
            )
        )

        # Create record of comment.
        payload = {
            "stream_uuid": active_stream_uuid,
            "status": Comment.STATUS_LEFT,
            "text": None,
        }
        _cache = await (
            Comment.objects.create_from_payload_async(_user, payload, _cache=_cache)
        )

        await self.channel_layer.group_send(  # TODO: put as manager method
            _cache["stream"].chat_room,
            {
                "type": "broadcast",
                "text": json.dumps(
                    {
                        "data": {
                            "comments": [Comment.objects.serialize(_cache["comment"], ticket=ticket)]
                        }
                    }
                ),
            },
        )

    # - - - - - -
    # HELPERS
    # - - - - - -

    async def websocket_accept(self):
        await self.send({"type": "websocket.accept"})

    async def add_to_channel(self, channel_name):
        await (
            self.channel_layer.group_add(channel_name, self.channel_name)
        )

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

    async def send_stream_status(self, stream_uuid, status):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({
                    "data": {
                        "stream": {
                            "status": status,
                            "uuid": stream_uuid,
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
                        ]
                    }
                }),
            }
        )
