import asyncio
import json
import requests
import uuid
from urllib.parse import urlparse

from datetime import datetime
from datetime import timedelta

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.serializers import serialize


from proj.apps.music.models import Ticket
from proj.apps.music.models import Comment
from proj.apps.users.models import Profile
from proj.apps.music.models import Showing
from proj.core.resources.cache import _get_or_fetch_from_cache
from proj.core.fns import results


class Consumer(AsyncConsumer):

    # - - - -
    # connect
    # - - - -

    async def websocket_connect(self, event):
        '''
        '''
        _cache = {}
        _user = self.scope['user']

        active_showing_uuid = self.scope['query_string'][5:].decode('utf-8')
        _cache = await Profile.objects.join_showing_async(
                _user, active_showing_uuid, _cache=_cache,
        )
        _user_profile = _cache['profile']
        ticket = _cache['ticket']

        await (
            self.channel_layer
            .group_add(_cache['showing'].chat_room, self.channel_name)
        )

        await self.send({
            'type': 'websocket.accept',
        })

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'data': {
                    'ticket': Ticket.objects.serialize(ticket),
                }
            }),
        })

        # Create record of comment.
        join_payload = {
            'showing_uuid': active_showing_uuid,
            'status': Comment.STATUS_JOINED,
            'text': None,
        }
        _cache = await (
            Comment.objects
            .create_from_payload_async(_user, join_payload, _cache=_cache)
        )
        comment = _cache['comment']

        # tell the chatroom that the user has joined
        await self.channel_layer.group_send(  # TODO: put as manager method
            _cache['showing'].chat_room,
            {
                'type': 'broadcast',
                'text': json.dumps({
                    'data': {
                        'comments': [
                            Comment.objects.serialize(_cache['comment'], ticket=ticket),
                        ],
                    }
                }),
            }
        )

        print('success connecting!')

        # get active record, if it exists
        now = datetime.now()
        try:
            showing = await database_sync_to_async(Showing.objects.select_related('current_record').get)(
                uuid=active_showing_uuid,
                status=Showing.STATUS_ACTIVATED,
                current_record__isnull=False,
                record_terminates_at__gt=(now + timedelta(seconds=5)),
            )
        except Exception as e:
            print('no active record')
            print('returning')
            return

        # get the now playing target progress in ms
        try:
            now_playing = await database_sync_to_async(
                Comment
                .objects
                .select_related('track')
                .filter(
                    created_at__lte=now,
                    showing__uuid=active_showing_uuid,
                    status=Comment.STATUS_START,
                )
                .order_by('-created_at')
                .first
            )()

        except Exception as e:
            print('no active track')
            print('WARNING: this edge case should not be hit.')
            print('returning')

        assert now_playing

        expected_ms = (
            (
                now_playing.created_at.replace(tzinfo=None) - now
            ).total_seconds() * 1000
        )

        # get the actual progress in ms
        try:
            user_spotify_access_token = _user_profile.spotify_access_token
            response = requests.get(
                'https://api.spotify.com/v1/me/player/currently-playing',
                headers={
                    'Authorization': f'Bearer {user_spotify_access_token}',
                    'Content-Type': 'application/json',
                },
            )

            response_json = response.json()

            spotify_ms = response_json['progress_ms']
            spotify_uri = response_json['item']['uri']
            spotify_is_playing = response_json['is_playing']

            track_is_already_playing = (
                spotify_is_playing and
                spotify_uri == now_playing.track.spotify_uri and
                abs(expected_ms + spotify_ms) < 5000
            )

            record_is_over = False  # abs(spotify_ms + expected_ms) > 5000
            if track_is_already_playing or record_is_over:
                # if within N second(s), leave be
                return
        except Exception as e:
            print('undocumented spotify error')
            print(e)
            print('returning')
            return

        # get other tracks to play in future
        record = showing.current_record
        uris = await database_sync_to_async(
            record
            .tracks_through
            .order_by
        )('number')

        uris = await database_sync_to_async(
            uris.values_list
        )('track__spotify_uri', flat=True)
        uris = await database_sync_to_async(list)(uris)
        while(uris):
            if uris[0] == now_playing.track.spotify_uri:
                break
            uris = uris[1:]

        if not uris:
            return

        await self.play_tracks(
            user_spotify_access_token,
            {
                'action': 'play',
                'data': {'uris': uris, 'position_ms': -expected_ms},
            }
        )

    # - - - - -
    # receieve
    # - - - - -

    async def websocket_receive(self, event):
        payload = json.loads(event['text'])
        _user = self.scope['user']
        _cache = {}

        # Validate request payload.
        is_valid, _cache = await (
            Comment.objects
            .validate_create_comment_payload_async(_user, payload)
        )
        if is_valid == results.RESULT_FAILED_VALIDATION:
            return
        elif is_valid == results.RESULT_PERFORM_SIDE_EFFECT_ONLY:
            # Display initial chat content.
            comments = await Comment.objects.list_comments_async(
                _cache['showing'], payload['most_recent_comment_timestamp']
            )
            comments = [
                Comment.objects.serialize(comment)
                for comment in comments
            ]
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'data': {'comments': comments}}),
            })
            return

        # Create record of comment.
        _cache = await (
            Comment.objects
            .create_from_payload_async(_user, payload, _cache=_cache)
        )

        showing = await database_sync_to_async(Showing.objects.get)(uuid=payload['showing_uuid'])
        _cache['showing'] = showing

        ticket = await database_sync_to_async(Ticket.objects.get)(
            holder=_user,
            showing=_cache['showing'],
        )

        await self.channel_layer.group_send(  # TODO: put as manager method
            _cache['showing'].chat_room,
            {
                'type': 'broadcast',
                'text': json.dumps({
                    'data': {
                        'comments': [
                            Comment.objects
                            .serialize(_cache['comment'], ticket=ticket)
                        ],
                    }
                }),
            }
        )

        if payload['status'] == Comment.STATUS_LEFT:
            # If leaving the chat, send final comment response back to original
            # user.
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({
                    'comments': [
                        Comment.objects
                        .serialize(_cache['comment'])
                    ]
                }),
            })
            return

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def broadcast(self, event):
        '''
        '''
        _user = self.scope['user']

        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

        _profile = await database_sync_to_async(Profile.objects.get)(user=_user)

        user_spotify_access_token = _profile.spotify_access_token
        try:
            if bool(event['playback']) and bool(user_spotify_access_token):
                await self.play_tracks(user_spotify_access_token, event['playback'])
        except:
            pass

    async def play_tracks(self, sat, playback):
        action = playback['action']
        data = json.dumps(playback['data']) or {}
        response = requests.put(
            f'https://api.spotify.com/v1/me/player/{action}',
            data=data,
            headers={
                'Authorization': f'Bearer {sat}',
                'Content-Type': 'application/json',
            },
        )


    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):
        _cache = {}
        _user = self.scope['user']
        await Profile.objects.leave_showing_async(_user)
        active_showing_uuid = self.scope['query_string'][5:].decode('utf-8')
        showing = await database_sync_to_async(Showing.objects.get)(uuid=active_showing_uuid)
        _cache['showing'] = showing

        await (
            self.channel_layer
            .group_discard(_cache['showing'].chat_room, self.channel_name)
        )

        # Create record of comment.
        payload = {
            'showing_uuid': active_showing_uuid,
            'status': Comment.STATUS_LEFT,
            'text': None,
        }
        _cache = await (
            Comment.objects
            .create_from_payload_async(_user, payload, _cache=_cache)
        )

        await self.channel_layer.group_send(  # TODO: put as manager method
            _cache['showing'].chat_room,
            {
                'type': 'broadcast',
                'text': json.dumps({
                    'data': {
                        'comments': [
                            Comment.objects
                            .serialize(_cache['comment'])
                        ]
                    }
                }),
            }
        )
