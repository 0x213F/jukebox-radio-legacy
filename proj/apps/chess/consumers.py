import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.serializers import serialize

from proj.apps.chess.models import ChessGame


class ChessGameConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        game = await database_sync_to_async(
            ChessGame.objects.belong_to(self.scope['user']).get
        )()
        self.group_name = game.group_name

        await self.channel_layer.group_add(
            game.group_name,
            self.channel_name,
        )

        await self.send({
            'type': 'websocket.accept',
        })

        try:
            game = await database_sync_to_async(
                ChessGame.objects.get_websocket_private_game
            )(self.scope['user'])
            response = await database_sync_to_async(
                ChessGame.objects.websocket_response
            )(game, self.scope['user'])
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(response),
            })
        except ChessGame.DoesNotExist:
            await self.send({
                'type': 'websocket.send',
                'text': 'ChessGame.DoesNotExist',
            })

        # await self.send({
        #     'type': 'websocket.send',
        #     'text': 'hello, world'
        # })

        # await self.send({
        #     'type': 'websocket.close'
        # })

    async def websocket_receive(self, event):

        game = await database_sync_to_async(
            ChessGame.objects.get_websocket_private_game
        )(self.scope['user'])

        if not game.is_users_turn(self.scope['user']):
            raise Exception('It is the opponent\'s turn')

        print(json.loads(event['text'])['uci'])

        result = ChessGame.objects.move_piece(game, json.loads(event['text'])['uci'])
        response = await database_sync_to_async(
            ChessGame.objects.websocket_response
        )(game, self.scope['user'])

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast',
                'text': json.dumps(response),
            }
        )

    async def broadcast(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

    async def websocket_disconnect(self, event):
        print('disconnect', event)
