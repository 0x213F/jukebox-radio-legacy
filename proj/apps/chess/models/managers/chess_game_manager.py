
import chess
import json
import random
import string

from datetime import datetime

from django.db.models import F
from django.db.models import Q

from proj.apps.chess.utils.decorators import get_game_by_user
from proj.apps.chess.utils.decorators import get_game_by_uuid
from proj.apps.chess.utils.decorators import assert_game_started
from proj.apps.chess.utils.decorators import assert_user_no_active_game
from proj.apps.chess.utils.decorators import assert_user_status_my_turn
from proj.apps.chess.utils.decorators import assert_user_status_their_turn

from proj.core.models.managers import BaseManager


class ChessGameManager(BaseManager):
    '''
    Engine that controls a game of chess.
    '''

    def response(self, game):
        '''
        Tranform a `ChessGame` object into a JSON response with additional
        context from relevant `ChessSnapshot` objects.
        '''
        from proj.apps.chess.models import ChessSnapshot

        snapshots = ChessSnapshot.objects.filter(
            game=game,
            step__gte=game.steps,  # the `gt` part includes suggested moves
        )

        return {
            'game': super().response([game]),
            'snapshots': super().response(snapshots),
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

    @assert_user_no_active_game
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

        game.take_snapshot(user, ChessSnapshot.ACTION_CREATE_MATCH)

        return game

    @assert_user_no_active_game
    def join_match(self, *, user=None, join_code=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API

        Have a user join game by authenticating with a pending `join_code`.
        '''
        from proj.apps.chess.models import ChessSnapshot
        ChessGame = self.model

        game = ChessGame.objects.get_by_join_code(join_code)
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
        game.take_snapshot(user, ChessSnapshot.ACTION_JOIN_MATCH)

        return game

    @get_game_by_user
    def close_match(self, *, game=None, user=None):
        '''
        PUBLIC METHOD ACCESSIBLE BY API
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        if (
            game.black_status == ChessGame.STATUS_MY_TURN or
            game.white_status == ChessGame.STATUS_MY_TURN
        ):
            raise Exception('Game has already started.')

        game.take_snapshot(user, ChessSnapshot.ACTION_CLOSE_MATCH)

        return self.end(game)

    @get_game_by_user
    @assert_game_started
    def resign_match(self, *, game=None, user=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API
        '''
        from proj.apps.chess.models import ChessSnapshot

        game.take_snapshot(user, ChessSnapshot.ACTION_RESIGN_MATCH)

        return self.end(game)

    # - - - - - -
    # game state
    # - - - - - -

    @get_game_by_user
    def take_move(self, *, game=None, user=None, uci=None):
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

        player = game.get_color(user)
        opponent = game.get_opponent(user)

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

        game.take_snapshot(user, ChessSnapshot.ACTION_TAKE_MOVE)

        game.board = updated_board
        game.steps += 1
        setattr(game, f'{player}_time', player_time)
        setattr(game, f'{player}_status', self.model.STATUS_THEIR_TURN)
        setattr(game, f'{opponent}_status', self.model.STATUS_MY_TURN)
        game.save()

        return game

    def undo_move(self):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API

        User may not directly undo a move without opponent's confirmation.
        '''
        raise NotImplementedError()

    @get_game_by_uuid
    def suggest_move(self, *, game=None, user=None, uci=None, uuid=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API
        '''
        from proj.apps.chess.models import ChessSnapshot

        updated_board = self.move(uci)

        game.take_snapshot(
            user,
            ChessSnapshot.ACTION_SUGGEST_MOVE,
            step=(game.steps + 1)
        )

    # - - - - - -
    # undo state
    # - - - - - -

    @get_game_by_user
    @assert_game_started
    @assert_user_status_their_turn
    def create_undo_request(self, *, game=None, user=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API
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

        game.take_snapshot(user, ChessSnapshot.ACTION_CREATE_UNDO_REQUEST)

        return game

    @get_game_by_user
    @assert_game_started
    @assert_user_status_my_turn
    def approve_undo_request(self, *, game=None, user=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        # TODO refactor this
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

        game.take_snapshot(user, ChessSnapshot.ACTION_APPROVE_UNDO_REQUEST)

        latest_move = ChessSnapshot.objects.filter(
            game=game,
            step=(game.steps-1),
            action=ChessSnapshot.ACTION_TAKE_MOVE,
        ).latest('created_at')

        if not latest_move:
            raise RuntimeError(
                'An undo request was successfully approved, but no latest '
                'move was found.'
            )

        player = game.get_color(user)
        opponent = game.get_opponent(user)

        game.board = latest_move.board
        game.steps -= 1
        setattr(game, f'{player}_status', self.model.STATUS_THEIR_TURN)
        setattr(game, f'{opponent}_status', self.model.STATUS_MY_TURN)
        game.save()

        return game

    @get_game_by_user
    @assert_game_started
    @assert_user_status_my_turn
    def reject_undo_request(self, *, game=None, user=None):
        '''
        !!!!!!  PUBLIC METHOD ACCESSIBLE BY API
        '''
        ChessGame = self.model
        from proj.apps.chess.models import ChessSnapshot

        # TODO refactor this
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

        game.take_snapshot(user, ChessSnapshot.ACTION_REJECT_UNDO_REQUEST)

        return game
