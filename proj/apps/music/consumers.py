import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.serializers import serialize


from proj.apps.music.models import Comment
from proj.apps.users.models import Profile


class ShowingConsumer(AsyncConsumer):

    # - - - - - - - - -
    # websocket methods
    # - - - - - - - - -

    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        payload = json.loads(event['text'])
        self.scope['user']
        await database_sync_to_async(
                Comment.objects.create
            )(
                status=payload['status'],
                text=payload['text'],
                showing_id=payload['showing_id'],
                track_id=payload['track_id'],
                commenter=self.scope['user'],
                timestamp=4.0,
            )
        if payload['status'] == Comment.STATUS_LEFT:
            await database_sync_to_async(
                    Profile.objects.filter(user=self.scope['user']).update
                )(
                    active_showing_id=None,
                )
        else:
            if payload['status'] == Comment.STATUS_LEFT:
                await database_sync_to_async(
                        Profile.objects.filter(user=self.scope['user']).update
                    )(
                        active_showing_id=payload['showing_id'],
                    )
        # await database_sync_to_async(
        #         Profile.objects.get(user=self.scope['user']).update
        #     )(
        #         active_showing_id=payload['showing_id']
        #     )
        print(payload)
        pass


    async def broadcast(self, event):
        pass
        # await self.send({
        #     'type': 'websocket.send',
        #     'text': event['text'],
        # })

    async def websocket_disconnect(self, event):
        pass

    # - - - - - - -
    # route methods
    # - - - - - - -

    # @database_sync_to_async
    # def move_piece(self):
    #     game = ChessGame.objects.active().belongs_to(self.scope['user']).get()
    #     if not game.is_users_turn(self.scope['user']):
    #         raise Exception('It is the opponent\'s turn')
    #     return ChessGame.objects.move_piece(game, data['uci'])
    #
    #
    # @database_sync_to_async
    # def join_match(self):
    #     game = ChessGame.objects.active().belongs_to(self.scope['user']).get()
    #     if not game.is_users_turn(self.scope['user']):
    #         raise Exception('It is the opponent\'s turn')
    #     return ChessGame.objects.move_piece(game, data['uci'])
