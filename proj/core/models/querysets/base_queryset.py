
from django.db import models
from django.db.models import Q


class BaseQuerySet(models.QuerySet):
    '''
    Inherits from Django QuerySet.
    '''

    def get_singular(self):
        '''
        Get the singular object from a QuerySet which is expected to only have
        1 object.
        '''
        if self.count() == 1:
            return self.first()
        raise Exception('Multiple objects found.')
