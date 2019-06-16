import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


from proj.apps.chess.models import ChessGame


class ChessGameConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        user = self.scope['user']
        game = await database_sync_to_async(
            ChessGame.objects.belong_to(user).get
        )()
        self.group_name = game.group_name

        await self.channel_layer.group_add(
            game.group_name,
            self.channel_name,
        )

        await self.send({
            'type': 'websocket.accept'
        })

        # await self.send({
        #     'type': 'websocket.send',
        #     'text': 'hello, world'
        # })

        # await self.send({
        #     'type': 'websocket.close'
        # })

    async def websocket_receive(self, event):

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast',
                'text': json.dumps({'foo': 'bar'}),
            }
        )

    async def broadcast(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

    async def websocket_disconnect(self, event):
        print('disconnect', event)
