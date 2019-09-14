import asyncio
import json
import requests
import uuid

from datetime import datetime
from datetime import timedelta

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.serializers import serialize


from proj.apps.music.models import Comment
from proj.apps.users.models import Profile
from proj.apps.music.models import Showing


class Consumer(AsyncConsumer):

    # - - - -
    # connect
    # - - - -

    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept',
        })

    # - - - - -
    # receieve
    # - - - - -

    async def websocket_receive(self, event):
        payload = json.loads(event['text'])
        _user = self.scope['user']
        _cache = {}

        is_valid = Comment.objects.validate_create_comment_request(_user, payload)
        if is_valid == Comment.RESULT_INCONCLUSIVE:
            is_valid = (
                Comment.objects
                .validate_create_comment_request_async(_user, payload)
            )
            if is_valid != Comment.RESULT_TRUE:
                return

        if payload['status'] == Comment.STATUS_JOINED:
            _cache = await (
                Profile.objects.join_showing_async(
                    _user, payload['showing_uuid'], _cache=_cache
                )
            )
            await (
                self.channel_layer
                .group_add(_cache['showing'].chat_room, self.channel_name)
            )
        elif payload['status'] == Comment.STATUS_LEFT:
            await Profile.objects.leave_showing_async(_user)
            print('left')
            print(_cache['showing'])
            await (
                self.channel_layer
                .group_discard(_cache['showing'].chat_room, self.channel_name)
            )

        await (
            Comment.objects
            .create_from_payload_async(_user, payload, _cache=_cache)
        )

        await self.channel_layer.group_send(  # TODO: put as manager method
            _cache['showing'].chat_room,
            {
                'type': 'broadcast',
                'text': json.dumps({
                    'comments': [
                        Comment.objects
                        .serialize(_cache['comment'], _cache['ticket'])
                    ]
                }),
            }
        )

        if payload['status'] == Comment.STATUS_JOINED:
            comments = await Comment.objects.list_comments_async(
                _user, _cache['showing'], payload['most_recent_comment_timestamp']
            )
            comments = [
                Comment.objects.serialize(_cache['comment'], _cache['ticket'])
                for comment in comments
            ]
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'comments': comments}),
            })

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def broadcast(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

        action = print(json.loads(event['text'])['comments'][0]['status'])
        is_change_player_action = action in Comment.STATUS_PLAYER_CHOICES
        if not is_change_player_action:
            return

        user_spotify_access_token = (
            self.scope['user']
            .profile.spotify_access_token
        )

        if action == 'play_track':
            Track.objects.play_track(action, user_spotify_access_token)
        elif action == 'pause_track':
            Track.objects.pause_track(action, user_spotify_access_token)
        elif action == 'next_track':
            Track.objects.next_track(action, user_spotify_access_token)
        elif action == 'prev_track':
            Track.objects.prev_track(action, user_spotify_access_token)


    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):
        pass
