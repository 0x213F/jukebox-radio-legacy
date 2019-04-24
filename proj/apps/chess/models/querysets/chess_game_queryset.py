
from django.db import models
from django.db.models import Q

from proj.core.models.querysets import BaseQuerySet


class ChessGameQuerySet(BaseQuerySet):
    '''
    Query methods to retrieve `ChessGame` objects from the database.
    '''

    def active(self, code=None):
        '''
        `ChessGame` objects that are active.
        '''
        return self.filter(finished_at__isnull=True)

    def belong_to(self, *users):
        '''
        `ChessGame` objects that belong to certain users.
        '''
        return self.filter(Q(black_user__in=users) | Q(white_user__in=users))

    def get_by_join_code(self, join_code):
        '''
        Get singular `ChessGame` object which matches the supplied `join_code`
        and is active.
        '''
        return self.active().filter(join_code=join_code).get_singular()
