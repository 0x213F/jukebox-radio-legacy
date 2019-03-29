
from django.db import models
from django.db.models import Q


class BaseQuerySet(models.QuerySet):
    '''
    todo: docstring
    '''

    def assert_singular(self):
        '''
        todo: docstring
        '''
        if self.count() == 1:
            return self
        raise Exception('Multiple objects found.')
