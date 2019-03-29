
import chess
import json
import random
import string

from datetime import datetime

from django.db import models


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
            black_status=ChessGame.STATUS_GAME_COMPLETE,
            white_status=ChessGame.STATUS_GAME_COMPLETE,
        )

    # - - - - - - - -
    # static methods
    # - - - - - - - -

    @staticmethod
    def generate_code():
        '''
        todo: docstring
        '''
        from proj.apps.chess.models import ChessGame
        return random.sample(
            string.ascii_lowercase + string.digits,
            ChessGame.CODE_LENGTH
        )

    ''' ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

    PUBLIC METHODS ACCESSIBLE BY API

    ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! '''

    # - - - - - - -
    # game status
    # - - - - - - -

    def join_match(self, game, user, **kwargs):
        '''
        Validates, then allows user to join match.
        '''

        if game:
            raise Exception('Already in a game.')

        join_code = kwargs.pop('join_code', None)
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
            board=game.board,
            game=game,
            step=game.steps,
        )

        return game

    def close_match(self, game, user, **kwargs):
        '''
        todo: docstring
        '''

        if not game:
            raise Exception('Not in game.')

        player = game.get_player(user)

        ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_CLOSE_MATCH,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

        return self._end(game)

    def resign(self, game, user, **kwargs):
        '''
        todo: docstring
        '''

        if not game:
            raise Exception('Not in game.')

        player = game.get_player(user)

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

    def take_move(self, game, user, **kwargs):
        '''
        todo: docstring
        '''

        if not game:
            raise Exception('Not in game.')

        player = game.get_player(user)

        latest_move = (
            game.snapshots.
            filter(
                action__in=[
                    ChessSnapshot.ACTION_TAKE_MOVE,
                    ChessSnapshot.ACTION_ASK_UNDO_REQUEST,
                ],
                game=game,
            ).
            latest('created_at')
        )

        lost_time = (datetime.now() - latest_move.created_at).total_seconds()
        time_left = getattr(game, f'{player}_time') - lost_time
        if time_left < 0:
            raise Exception('The player has run out of time.')

        try:
            uci = kwargs.pop('uci')
            move_obj = chess.Move.from_uci(uci)

            board = chess.Board(game.board)
            board.push(move_obj)
            updated_board = board.fen()

        except Exception:
            raise Exception('Invalid move.')

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
        })

    def undo_move(self, **kwargs):
        '''
        todo: docstring
        '''
        pass

    def suggest_move(self, game, user, **kwargs):
        '''
        todo: docstring
        '''

        try:
            uci = kwargs.pop('uci')
            move_obj = chess.Move.from_uci(uci)

            board = chess.Board(game.board)
            board.push(move_obj)
            updated_board = board.fen()

        except Exception:
            raise Exception('Invalid move.')

        return ChessSnapshot.objects.create(
            action=ChessSnapshot.ACTION_SUGGEST_MOVE,
            actor=user,
            board=game.board,
            game=game,
            step=game.steps,
        )

    # - - - - - -
    # undo state
    # - - - - - -

    def ask_undo_request(self, game, user, **kwargs):
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
