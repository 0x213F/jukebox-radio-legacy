
import chess
import json
import random
import string

from datetime import datetime

from django.core.serializers import serialize
from django.db.models import F
from django.db.models import Q

from proj.core.models.managers import BaseManager


class ChessGameManager(BaseManager):
    '''
    todo: docstring
    '''

    def response(self, game, request):
        '''
        todo: docstring
        '''
        from proj.apps.chess.models import ChessSnapshot

        snapshots = ChessSnapshot.objects.filter(game=game)

        return {
            'game': json.loads(serialize('json', [game])[1:-1]),
            'snapshots': json.loads(serialize('json', snapshots)),
            'user': json.loads(serialize('json', [request.user])[1:-1]),
        }

    def websocket_response(self, game, user):
        '''
        todo: docstring
        '''
        from proj.apps.chess.models import ChessSnapshot

        snapshots = ChessSnapshot.objects.filter(game=game)

        return {
            'game': json.loads(serialize('json', [game])[1:-1]),
            'snapshots': json.loads(serialize('json', snapshots)),
            'user': json.loads(serialize('json', [user])[1:-1]),
        }

    # - - - - - - - -
    # helper methods
    # - - - - - - - -

    def end(self, game):
        '''
        todo: docstring
        '''
        ChessGame = self.model

        ChessGame.objects.filter(id=game.id).update(
            finished_at=datetime.now(),
            black_status=ChessGame.STATUS_COMPLETE,
            white_status=ChessGame.STATUS_COMPLETE,
        )

        game.refresh_from_db()
        return game

    # - - - - - - - -
    # static methods
    # - - - - - - - -

    def _generate_code(self):
        '''
        todo: docstring
        '''
        return ''.join(random.sample(
            string.ascii_lowercase + string.digits,
            self.model.JOIN_CODE_LENGTH
        ))

    @staticmethod
    def move(game, uci):
        move_obj = chess.Move.from_uci(uci)
        board = chess.Board(game.board)
        board.push(move_obj)
        return board.fen()

    # - - - - - - -
    # game status
    # - - - - - - -

    def create_match(self, *, user=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API

        Endpoint create method to allow user to create a `ChessGame`.
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        data = {
            'board': chess.Board().fen(),
            'is_private': True,
        }
        player = random.choice(list(ChessGame.COLOR_CHOICES))
        opponent = 'white' if player == 'black' else 'black'

        data[f'{player}_user'] = user
        data[f'{player}_status'] = ChessGame.STATUS_PENDING_WAITING
        data[f'{opponent}_status'] = ChessGame.STATUS_PENDING_OPPONENT

        # randomly generate a valid code
        while True:
            join_code = self._generate_code()
            if ChessGame.objects.active().filter(join_code=join_code).exists():
                continue
            break
        data['join_code'] = join_code

        game =  super().create(**data)

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_CREATE_MATCH,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        return game

    def join_match(self, user, join_code):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API

        Have a user join game by authenticating with a pending `join_code`.
        '''
        from proj.apps.chess.models import ChessSnapshot
        ChessGame = self.model

        game = ChessGame.objects.join_code(join_code)
        if join_code != game.join_code:
            raise Exception('Invalid join code.')

        if not game.black_user:
            game.black_user = user
        elif not game.white_user:
            game.white_user = user
        else:
            raise Exception('Game already has 2 players.')

        game.black_status = ChessGame.STATUS_THEIR_TURN
        game.white_status = ChessGame.STATUS_MY_TURN

        game.save()
        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_JOIN_MATCH,
            actor=user,
            game=game,
            step=game.steps,
        )

        return game

    def close_match(self, game, user):
        '''
        todo
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        if (
            game.black_status == ChessGame.STATUS_MY_TURN or
            game.white_status == ChessGame.STATUS_MY_TURN
        ):
            raise Exception('Game has already started.')

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_CLOSE_MATCH,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        return self.end(game)

    def resign_match(self, game):
        '''
        todo
        '''
        from proj.apps.chess.models import ChessSnapshot

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_RESIGN_MATCH,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        return self.end(game)

    # - - - - - -
    # game state
    # - - - - - -

    def move_piece(self, game, uci):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        try:
            latest_move = game.snapshots.latest_move(game)
            lost_time = (
                datetime.now() -
                latest_move.created_at.replace(tzinfo=None)
            ).total_seconds()
        except ChessSnapshot.DoesNotExist:
            lost_time = 0

        user = game.get_user_status_my_turn
        player = game.get_users_color(user)
        opponent = game.get_users_opponent(user)

        time_left = getattr(game, f'{player}_time') - lost_time
        if time_left < 0:
            raise Exception('The player has run out of time.')

        is_players_turn = (
            getattr(game, f'{player}_status') == ChessGame.STATUS_MY_TURN
        )
        if not is_players_turn:
            raise Exception('It is not the player\'s turn.')

        updated_board = self.move(game, uci)
        player_time = getattr(game, f'{player}_time') - lost_time

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_TAKE_MOVE,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        game.board = updated_board
        game.steps += 1
        setattr(game, f'{player}_time', player_time)
        setattr(game, f'{player}_status', self.model.STATUS_THEIR_TURN)
        setattr(game, f'{opponent}_status', self.model.STATUS_MY_TURN)
        game.save()

        return game

    def suggest_move(self, *, game=None, user=None, uci=None, uuid=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API
        '''
        from proj.apps.chess.models import ChessSnapshot

        updated_board = self.move(uci)

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_SUGGEST_MOVE,
            actor=user,
            board=updated_board,
            game=game,
            step=(game.steps + 1),
        )

    # - - - - - -
    # undo state
    # - - - - - -

    def ask_undo(self, game, user):
        '''
        todo
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        last_create_undo_request = None
        try:
            last_create_undo_request = (
                ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_CREATE_UNDO_REQUEST)
            )
        except ChessSnapshot.DoesNotExist:
            pass

        if last_create_undo_request:
            try:
                last_reject_undo_request = (
                    ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_REJECT_UNDO_REQUEST)
                )
                if last_create_undo_request.created_at > last_reject_undo_request.created_at:
                    last_approve_undo_request = (
                        ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_APPROVE_UNDO_REQUEST)
                    )
                    if last_create_undo_request.created_at > last_approve_undo_request.created_at:
                        raise Exception('Request still pending.')

            except ChessSnapshot.DoesNotExist:
                try:
                    last_approve_undo_request = (
                        ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_APPROVE_UNDO_REQUEST)
                    )
                    if last_create_undo_request.created_at > last_approve_undo_request.created_at:
                        raise Exception('Request still pending.')
                except ChessSnapshot.DoesNotExist:
                    raise Exception('Request still pending.')

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_CREATE_UNDO_REQUEST,
            actor=user,
            game=game,
            step=game.steps,
        )

        return game

    def approve_undo(self, game, user):
        '''
        todo
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        last_create_undo_request = None
        try:
            last_create_undo_request = (
                ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_CREATE_UNDO_REQUEST)
            )
        except ChessSnapshot.DoesNotExist:
            raise Exception('No undo was requested.')

        try:
            last_reject_undo_request = (
                ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_REJECT_UNDO_REQUEST)
            )
            if last_create_undo_request.created_at < last_reject_undo_request.created_at:
                raise Exception('No undo was requested.')
        except ChessSnapshot.DoesNotExist:
            pass

        try:
            last_approve_undo_request = (
                ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_APPROVE_UNDO_REQUEST)
            )
            if last_create_undo_request.created_at < last_approve_undo_request.created_at:
                raise Exception('No undo was requested.')
        except ChessSnapshot.DoesNotExist:
            pass

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_APPROVE_UNDO_REQUEST,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        latest_move = ChessSnapshot.objects.filter(
            game=game,
            step=(game.steps-1),
            action=ChessSnapshot.ACTION_TAKE_MOVE,
        ).latest('created_at')
        player = game.get_users_color(user)
        opponent = game.get_users_opponent(user)

        game.board = latest_move.board
        game.steps -= 1
        setattr(game, f'{player}_status', self.model.STATUS_THEIR_TURN)
        setattr(game, f'{opponent}_status', self.model.STATUS_MY_TURN)
        game.save()

        return game

    def reject_undo(self, game, user):
        '''
        todo
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        last_create_undo_request = None
        try:
            last_create_undo_request = (
                ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_CREATE_UNDO_REQUEST)
            )
        except ChessSnapshot.DoesNotExist:
            raise Exception('No undo was requested.')

        try:
            last_reject_undo_request = (
                ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_REJECT_UNDO_REQUEST)
            )
            if last_create_undo_request.created_at < last_reject_undo_request.created_at:
                raise Exception('No undo was requested.')
        except ChessSnapshot.DoesNotExist:
            pass

        try:
            last_approve_undo_request = (
                ChessSnapshot.objects.latest_action(game, ChessSnapshot.ACTION_APPROVE_UNDO_REQUEST)
            )
            if last_create_undo_request.created_at < last_approve_undo_request.created_at:
                raise Exception('No undo was requested.')
        except ChessSnapshot.DoesNotExist:
            pass

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_REJECT_UNDO_REQUEST,
            actor=user,
            game=game,
            step=game.steps,
        )

        return game
