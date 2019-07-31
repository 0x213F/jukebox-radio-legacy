import asyncio
import json
import uuid

from datetime import datetime
from datetime import timedelta

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.serializers import serialize


from proj.apps.music.models import Comment
from proj.apps.users.models import Profile


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
        self.scope['user']
        showing_id = payload['showing_id']
        chatroom = f'showing-{showing_id}'
        self.chatroom = f'showing-{showing_id}'
        print(payload)
        await database_sync_to_async(
                Comment.objects.create
            )(
                status=payload['status'],
                text=payload['text'],
                showing_id=showing_id,
                track_id=payload['track_id'],
                commenter=self.scope['user'],
                timestamp=4.0,
            )
        showing_uuid = self.scope['user'].profile.showing_uuid
        if payload['status'] == Comment.STATUS_LEFT:
            await database_sync_to_async(
                    Profile.objects.filter(user=self.scope['user']).update
                )(
                    active_showing_id=None,
                    showing_uuid=None,
                )
            await self.channel_layer.group_discard(chatroom, self.channel_name)
        else:
            profile = await database_sync_to_async(
                    Profile.objects.get
                )(
                    user=self.scope['user']
                )
            showing_id = profile.active_showing_id
            if not showing_id:
                await self.channel_layer.group_add(
                    chatroom,
                    self.channel_name,
                )
                await database_sync_to_async(
                        Profile.objects.filter(user=self.scope['user']).update
                    )(
                        active_showing_id=payload['showing_id'],
                    )
            if not profile.showing_uuid:
                showing_uuid = str(uuid.uuid4())
                await database_sync_to_async(
                        Profile.objects.filter(user=self.scope['user']).update
                    )(
                        showing_uuid=showing_uuid,
                    )

        if payload['status'] not in ['waiting', 'joined'] or payload['text']:
            await self.channel_layer.group_send(
                chatroom,
                {
                    'type': 'broadcast',
                    'text': json.dumps({
                        'payload': payload,
                        'user': {
                            'display_name': self.scope['user'].profile.display_name,
                            'showing_uuid': showing_uuid,
                        },
                    }),
                }
            )

        if payload['status'] == 'joined':
            comments = await database_sync_to_async(
                    Comment.objects.select_related('commenter', 'commenter__profile').filter
                )(
                    created_at__gte=datetime.now() - timedelta(minutes=30),
                    showing_id=payload['showing_id'],
                )
            comments_obj = []
            for comment in comments:
                comments_obj.insert(0, {
                    'text': comment.text,
                    'status': comment.status,
                    'profile_showing_uuid': comment.commenter.profile.showing_uuid,
                    'profile_display_name': comment.commenter.profile.display_name,
                    'created_at': comment.created_at.isoformat(),
                })
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({
                    'payload': payload,
                    'user': {
                        'display_name': self.scope['user'].profile.display_name,
                        'showing_uuid': showing_uuid,
                    },
                    'comments': comments_obj,
                }),
            })

        pass

    # - - - - -
    # broadcast
    # - - - - -

    async def broadcast(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):
        # await self.channel_layer.group_discard("chat", self.channel_name)
        await database_sync_to_async(
                Profile.objects.filter(user=self.scope['user']).update
            )(
                active_showing_id=None,
            )
