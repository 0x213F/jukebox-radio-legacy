
from django.db import models
from django.db.models import Q

from proj.core.models.querysets import BaseQuerySet


class ChessGameQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query ChessGame objects.
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
        return self.filter(Q(black_user__in=users) | Q(white_user__in=users))

    def private(self):
        '''
        ChessGame objects that have the following access levels:

        - Player is in game: read and move. (selective write)
        - Has access to UUID: read and suggest. (selective write)
        '''
        return self.filter(is_private=False)

    def public(self):
        '''
        ChessGame objects that have the following access levels:

        - Has access to join code: read and suggest. (selective write)
        '''
        return self.filter(is_private=False)

    def join_code(self, join_code):
        '''
        ChessGame objects that match a given join code.
        '''
        return self.filter(join_code=join_code)
