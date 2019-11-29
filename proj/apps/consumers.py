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
from proj.core.resources.cache import _get_or_fetch_from_cache
from proj.core.fns import results


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

        print(payload)

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
                'text': json.dumps({'comments': comments}),
            })
            return

        if payload['status'] == Comment.STATUS_JOINED:
            # Add user to chat room.
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
            # Remove user from chat room.
            await Profile.objects.leave_showing_async(_user)
            _cache = _get_or_fetch_from_cache(
                _cache,
                'showing',
                fetch_func=Showing.objects.get,
                fetch_kwargs={'uuid': payload['showing_uuid']}
            )
            await (
                self.channel_layer
                .group_discard(_cache['showing'].chat_room, self.channel_name)
            )

        # Create record of comment.
        _cache = await (
            Comment.objects
            .create_from_payload_async(_user, payload, _cache=_cache)
        )

        _cache = _get_or_fetch_from_cache(
            _cache,
            'showing',
            fetch_func=Showing.objects.get,
            fetch_kwargs={'uuid': payload['showing_uuid']}
        )
        await self.channel_layer.group_send(  # TODO: put as manager method
            _cache['showing'].chat_room,
            {
                'type': 'broadcast',
                'text': json.dumps({
                    'comments': [
                        Comment.objects
                        .serialize(_cache['comment'])
                    ]
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

        if payload['status'] == Comment.STATUS_JOINED:
            # Display initial chat content.
            comments = await Comment.objects.list_comments_async(
                _cache['showing'], payload['most_recent_comment_timestamp']
            )
            comments = [
                # TODO: comments should be serialized with correct ticket
                Comment.objects.serialize(comment)
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

        user_spotify_access_token = (
            self.scope['user']
            .profile.spotify_access_token
        )
        if bool(event['tracks']) and bool(user_spotify_access_token):
            print('SPIN THAT DISK')


    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):
        pass
