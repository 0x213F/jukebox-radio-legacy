
import random
import string

from proj.core.models.managers import BaseManager


class TrackManager(BaseManager):
    '''
<<<<<<< HEAD:proj/apps/chess/models/managers/chess_snapshot_manager.py
    Engine that handles the history of a chess game.
=======
    Django QuerySet used to query ChessSnapshot objects.
>>>>>>> foo:proj/apps/music/models/managers/track_manager.py
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
