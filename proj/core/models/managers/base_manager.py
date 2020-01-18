import json

from channels.db import database_sync_to_async
from django.apps import apps
from django.core.serializers import serialize
from django.db import models

from proj.core.fns.etc import noop


class BaseManager(models.Manager):
    """
    Inherits from Django Manager.
    """

    def response(self, results):
        """
        Subclass this method to transform a response object into a JSON object.
        """
        results = json.loads(serialize("json", results))
        return results[0] if len(results) == 1 else results

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
