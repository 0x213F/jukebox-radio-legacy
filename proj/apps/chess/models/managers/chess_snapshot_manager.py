
import random
import string

from proj.core.models.managers import BaseManager


class ChessSnapshotManager(BaseManager):
    '''
    Engine that handles the history of a chess game.
    '''

    def take_snapshot(self, game, user, action, steps=None):
        ChessSnapshot = self.model
        steps = game.steps if not steps else steps
        return ChessSnapshot.objects.create(
            action=game,
            actor=user,
            board=game.board,
            game=game,
            step=steps,
        )
