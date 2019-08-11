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

        # Join the chat room
        if payload['status'] == Comment.STATUS_JOINED:
            await (
                Profile.objects
                .join_showing_async(_user, payload, _cache=_cache)
            )

        # Leave the chat room
        if payload['status'] == Comment.STATUS_LEFT:
            await Profile.objects.leave_showing_async(_user)
            await (
                self.channel_layer
                .group_discard(_cache['showing'].chat_room, self.channel_name)
            )

        # Save the comment to the database
        await (
            Comment.objects
            .create_from_payload_async(_user, payload, _cache=_cache)
        )

        # Spotify command
        spotify = {}
        if payload['status'] in (Comment.STATUS_PAUSE, Comment.STATUS_PLAY, Comment.STATUS_SKIP_FORWARD):
            spotify['action'] = payload['status']

        # Leave the chat room
        if payload['status'] == Comment.STATUS_LEFT:
            await Profile.objects.leave_showing(_user)
            await self.channel_layer.group_discard(_cache['showing'].chat_room, self.channel_name)

        # Ping the chat room
        await self.channel_layer.group_send(  # TODO: put as manager method
            _cache['showing'].chat_room,
            {
                'type': 'broadcast',
                'text': json.dumps({'comments': [Comment.objects.serialize(_cache['comment'], _cache['ticket'])]}),
                'spotify': spotify,
            }
        )

        # Join the chat room
        if payload['status'] == Comment.STATUS_JOINED:
            await (
                self.channel_layer
                .group_add(_cache['showing'].chat_room, self.channel_name)
            )
            comments = await Comment.objects.list_comments_async(_user, _cache['showing'], payload['most_recent_comment_timestamp'])
            comments = [Comment.objects.serialize(_cache['comment'], _cache['ticket']) for comment in comments]
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'comments': comments}),
            })

    # - - - - -
    # broadcast
    # - - - - -

    async def broadcast(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })
        try:
            spotify = event['spotify']
            context_uri = spotify['context_uri']
            spotify_access_token = self.scope['user'].profile.spotify_access_token
            response = requests.put(
                'https://api.spotify.com/v1/me/player/play',
                headers={
                    'Authorization': f'Bearer {spotify_access_token}',
                    'Content-Type': 'application/json',
                },
                data=json.dumps({
                    'context_uri': context_uri,
                })
            )
        except KeyError:
            pass
        try:
            spotify = event['spotify']
            action = spotify['action']
            if action != 'next':
                spotify_access_token = self.scope['user'].profile.spotify_access_token
                response = requests.put(
                    f'https://api.spotify.com/v1/me/player/{action}',
                    headers={
                        'Authorization': f'Bearer {spotify_access_token}',
                        'Content-Type': 'application/json',
                    },
                )
            else:
                spotify_access_token = self.scope['user'].profile.spotify_access_token
                response = requests.post(
                    f'https://api.spotify.com/v1/me/player/{action}',
                    headers={
                        'Authorization': f'Bearer {spotify_access_token}',
                        'Content-Type': 'application/json',
                    },
                )
        except KeyError:
            pass
    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):
        pass
