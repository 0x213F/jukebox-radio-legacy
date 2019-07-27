
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
        count = self.count()
        if count == 1:
            return self.first()
        elif count == 0:
            raise self.model.DoesNotExist()
        raise Exception('Multiple objects found.')

    def get_by_priority(self, priority_filters):
        for filter in priority_filters:
            try:
                return self.get(**filter)
            except self.model.DoesNotExist:
                pass
        raise self.model.DoesNotExist
