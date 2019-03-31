
from django.db import models
from django.db.models import Q


class ChessSnapshotQuerySet(models.QuerySet):
    '''
    todo: docstring
    '''

    def suggestions(self, game):
        return (
            self.filter(
                step__gt=game.steps,
                ChessSnapshot.ACTION_SUGGEST_MOVE,
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
                    ChessSnapshot.ACTION_ASK_UNDO_REQUEST,
                ],
                game=game,
            ).
            latest('created_at')
        )
