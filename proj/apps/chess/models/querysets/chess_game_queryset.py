
from django.db import models
from django.db.models import Q

from proj.core.models.querysets import BaseQuerySet


class ChessGameQuerySet(BaseQuerySet):
    '''
    todo: docstring
    '''

    # - - - - - - -
    # logic filters
    # - - - - - - -

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
        '''
        TODO docstring
        '''
        return self.filter(is_private=False)

    # - - - - - - - - -
    # business filters
    # - - - - - - - - -

    def join_code(self, join_code):
        '''
        TODO docstring
        '''
        return self.active().filter(join_code=join_code).get()

    def get_private_game(self, request):
        '''
        TODO docstring
        '''
        return self.active().belong_to(request.user).get()

    def get_websocket_private_game(self, user):
        '''
        TODO docstring
        '''
        return self.active().belong_to(user).get()
