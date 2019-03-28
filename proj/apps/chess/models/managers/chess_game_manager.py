
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
