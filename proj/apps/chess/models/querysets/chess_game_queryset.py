
from django.db import models
from django.db.models import Q

from proj.core.models.querysets import BaseQuerySet


class ChessGameQuerySet(BaseQuerySet):
    '''
    todo: docstring
    '''

    def active(self, code=None):
        '''
        ChessGame objects that are active.
        '''
        return self.filter(finished_at__isnull=True)

    def belong_to(self, *users):
        '''
        ChessGame objects that belong to certain users.
        '''
        return self.filter(Q(black_user__in=users) | Q(white_user__in=users))

    def private(self):
        return self.filter(is_private=False)

    def join_code(self, join_code):
        return self.active().filter(join_code=join_code).get_singular()
