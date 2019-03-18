
from django.db import models
from django.db.models import Q

class ChessQuerySet(models.QuerySet):

    def active(self, code=None):
        '''
        Chess objects that are active.
        '''
        return self.filter(finished_at__isnull=True)

    def belongs_to(self, *users):
        '''
        Chess objects that belong to certain users.
        '''
        return self.filter(Q(black__in=users) | Q(white__in=users))
