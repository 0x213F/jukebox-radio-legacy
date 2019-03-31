
import chess
import json
import random
import string

from datetime import datetime

from django.db import models


def validate_args(func):
    def validate(*args):
        if not all(args):
            raise Exception('Missing required parameters.')
        return func()
    return validate


@validate_args
def authenticate_game(func):
    def verify(game, user, **args, **kwargs):
        game.get_player(user)
        return func(game, user, *args, **kwargs)
    return verify


class ChessGameManager(models.Manager):
    '''
    todo: docstring
    '''

    # - - - - - - - -
    # helper methods
    # - - - - - - - -

    def _end(self, game):
        '''
        todo: docstring
        '''
        return game.update(
            finished_at=datetime.now(),
            black_status=self.model.STATUS_GAME_COMPLETE,
            white_status=self.model.STATUS_GAME_COMPLETE,
        )

    # - - - - - - - -
    # static methods
    # - - - - - - - -

    @staticmethod
    def generate_code():
        '''
        todo: docstring
        '''
        return random.sample(
            string.ascii_lowercase + string.digits,
            self.model.CODE_LENGTH
        )

    @staticmethod
    def move():
        move_obj = chess.Move.from_uci(uci)

        board = chess.Board(game.board)
        board.push(move_obj)
        updated_board = board.fen()

    ''' ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

    PUBLIC METHODS ACCESSIBLE BY API

    ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! '''

    # - - - - - - -
    # game status
    # - - - - - - -

    def join(self, user, *, join_code=None):
        '''
        Validates, then allows user to join match.
        '''

        active_games = (
            self.model.objects.
            active().
            belong_to(request.user)
        )
        if active_games.exists():
            raise Exception('Already in game.')

        if join_code != game.join_code:
            raise Exception('Invalid join code.')

        if not game.black:
            game.black = user
        elif not game.white:
            game.white = user
        else:
            raise Exception('Game already has 2 players.')

        game.save()

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_JOIN_MATCH,
            actor=user,
            game=game,
        )


    @authenticate_game
    def close_match(self, game, user):
        '''
        todo: docstring
        '''

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_CLOSE_MATCH,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        return self._end(game)

    @authenticate_game
    def resign(self, game, user):
        '''
        todo: docstring
        '''

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_RESIGN,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        return self._end(game)

    # - - - - - -
    # game state
    # - - - - - -

    @authenticate_game
    def take_move(self, game, user, *, uci=None):
        '''
        todo: docstring
        '''

        latest_move = game.snapshots.latest_move()
        lost_time = (datetime.now() - latest_move.created_at).total_seconds()

        player = game.get_player(user)
        opponent = game.get_opponent(user)

        time_left = getattr(game, f'{player}_time') - lost_time
        if time_left < 0:
            raise Exception('The player has run out of time.')

        updated_board = self.move(uci)

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_TAKE_MOVE,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        return game.update(**{
            'board': updated_board,
            'steps': F('steps') + 1,
            f'{player}_time': F(f'{player}_time') - lost_time,
            f'{player}_status': self.model.STATUS_THEIR_TURN,
            f'{opponent}_status': self.model.STATUS_MY_TURN,
        })

    def undo_move(self, game):
        '''
        todo: docstring
        '''
        pass


    @validate_args
    def suggest_move(self, user, *, uci=None, uuid=None):
        '''
        todo: docstring
        '''

        game = self.model.objects.get(uuid=uuid)
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

    @authenticate_game
    def ask_undo_request(self, game, user, **kwargs):
        '''
        todo: docstring
        '''
        return ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_ASK_UNDO_REQUEST,
            actor=user,
            game=game,
        )

    def approve_undo_request(self, **kwargs):
        '''
        todo: docstring
        '''

        player = game.get_player(user)

        return ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_ASK_UNDO_REQUEST,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

    def reject_undo_request(self, **kwargs):
        '''
        todo: docstring
        '''
        pass
