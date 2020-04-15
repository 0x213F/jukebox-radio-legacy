from datetime import datetime

from django.db import models
from django.db.models import Q


class BaseQuerySet(models.QuerySet):
    '''
    Inherits from Django QuerySet.
    '''

    def delete(self):
        self.update(deleted_at=datetime.utcnow())
