
from django.db import models
from django.db.models import F
from django.db.models import Q

from proj.core.models.querysets import BaseQuerySet


class ChessSnapshotQuerySet(BaseQuerySet):
    '''
    todo: docstring
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

    def latest_move(self):
        '''
        todo
        '''
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
