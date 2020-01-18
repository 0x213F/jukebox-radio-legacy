from datetime import datetime

from django.db import models
from django.db.models import Q


class BaseQuerySet(models.QuerySet):
    """
    Inherits from Django QuerySet.
    """

    def get_by_priority(self, *priority_filters):
        """
        Attempt to get an object multiple times with different filters.
        """
        for filter in priority_filters:
            try:
                return self.get(**filter)
            except self.model.DoesNotExist:
                pass
        raise self.model.DoesNotExist

    def delete(self):
        self.update(deleted_at=datetime.utcnow())
