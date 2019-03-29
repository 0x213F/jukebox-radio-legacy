
import chess
import json
import random
import string

from django.db import models


class ChessGameManager(models.Manager):
    '''
    todo: docstring
    '''

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

    def take_move(self, game, user):
        '''
        todo: docstring
        '''
        pass

    def suggest_move(self, game, user=None):
        '''
        todo: docstring
        '''
        pass

    def close_match(self, game, user=None):
        '''
        todo: docstring
        '''
        pass

    def resign(self, game, user):
        '''
        todo: docstring
        '''
        pass

    def decline_rematch(self, game, user):
        '''
        todo: docstring
        '''
        pass

    def submit_undo_request(self, game, user):
        '''
        todo: docstring
        '''
        pass

    def approve_undo_request(self, game, user):
        '''
        todo: docstring
        '''
        pass

    def reject_undo_request(self, game, user):
        '''
        todo: docstring
        '''
        pass

    def undo_move(self, game, user):
        '''
        todo: docstring
        '''
        pass
