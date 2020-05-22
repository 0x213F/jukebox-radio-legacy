import json

from channels.db import database_sync_to_async
from django.apps import apps
from django.core.serializers import serialize
from django.db import models


class BaseManager(models.Manager):
    """
    Inherits from Django Manager.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
