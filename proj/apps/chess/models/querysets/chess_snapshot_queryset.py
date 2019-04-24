
from django.db import models
from django.db.models import F
from django.db.models import Q

from proj.core.models.querysets import BaseQuerySet


class ChessSnapshotQuerySet(BaseQuerySet):
    '''
    Query methods to retrieve `ChessSnapshot` objects from the database.
    '''

    def suggestions(self, game):
        return (
            self.filter(
                step=(F(steps) + 1),
                action=ChessSnapshot.ACTION_SUGGEST_MOVE,
            )
        )

    def relevant(self):
        '''
        todo
        '''
        return self

    def latest_action(self, game, action):
        '''
        todo
        '''
        from proj.apps.chess.models import ChessSnapshot

        return (
            self.filter(
                action=action,
                game=game,
                step=game.steps,
            ).
            latest('created_at')
        )

    def latest_move(self, game):
        '''
        todo
        '''
        from proj.apps.chess.models import ChessSnapshot

        return (
            self.filter(
                action__in=[
                    ChessSnapshot.ACTION_TAKE_MOVE,
                    ChessSnapshot.ACTION_APPROVE_UNDO_REQUEST,
                ],
                game=game,
            ).
            latest('created_at')
        )
