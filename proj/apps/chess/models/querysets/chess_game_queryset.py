
from django.db import models
from django.db.models import Q


class ChessGameQuerySet(models.QuerySet):
    '''
    todo: docstring
    '''

    def active(self, code=None):
        '''
        ChessGame objects that are active.
        '''
        return self.filter(finished_at__isnull=True)

    def belongs_to(self, *users):
        '''
        ChessGame objects that belong to certain users.
        '''
        return self.filter(Q(black__in=users) | Q(white__in=users))
