
from django.db import models
from django.db.models import Q


class ChessSnapshotQuerySet(models.QuerySet):
    '''
    todo: docstring
    '''

    def most_recent(self):
        '''
        todo: docstring
        '''
        return self.order_by('+step')  # TODO only get most recent

    def get_popular_move(self, game):
        '''
        todo: docstring
        '''
        return (
            game.snapshots.most_recent.
            filter(
                action=ChessSnapshot.ACTION_SUGGEST_MOVE,
            )
        )
