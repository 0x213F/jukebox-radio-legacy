import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.serializers import serialize

from proj.apps.chess.models import ChessGame
from proj.apps.chess.models import ChessSnapshot


class ChessGameConsumer(AsyncConsumer):

    # - - - - - - - - -
    # websocket methods
    # - - - - - - - - -

    async def websocket_connect(self, event):
        game = await database_sync_to_async(
            ChessGame.objects.belongs_to(self.scope['user']).get
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
                ChessGame.objects.active().belongs_to(self.scope['user']).get
            )()
            data = await database_sync_to_async(
                ChessGame.objects.websocket_response
            )(game, self.scope['user'])
            route = 'redraw_board'

            payload = {
                'data': data,
                'route': route,
            }
            text = json.dumps(payload)
            await self.send({
                'type': 'websocket.send',
                'text': text,
            })
        except ChessGame.DoesNotExist:
            await self.send({
                'type': 'websocket.send',
                'text': 'ChessGame.DoesNotExist',
            })

    async def websocket_receive(self, event):

        payload = json.loads(event['text'])
        route = payload['route']
        data = payload['data']

        if route == ChessSnapshot.ACTION_TAKE_MOVE:
            response = self.move_piece(data)
        elif route == ChessSnapshot.ACTION_JOIN_MATCH:
            response = self.join_match(data)
    
            game = await database_sync_to_async(
                ChessGame.objects.belongs_to(self.scope['user']).get
            )()
            self.group_name = game.group_name

            await self.channel_layer.group_add(
                game.group_name,
                self.channel_name,
            )

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


    # - - - - - - -
    # route methods
    # - - - - - - -

    @database_sync_to_async
    def move_piece(self):
        game = ChessGame.objects.active().belongs_to(self.scope['user']).get()
        if not game.is_users_turn(self.scope['user']):
            raise Exception('It is the opponent\'s turn')
        return ChessGame.objects.move_piece(game, data['uci'])


    @database_sync_to_async
    def join_match(self):
        game = ChessGame.objects.active().belongs_to(self.scope['user']).get()
        if not game.is_users_turn(self.scope['user']):
            raise Exception('It is the opponent\'s turn')
        return ChessGame.objects.move_piece(game, data['uci'])
