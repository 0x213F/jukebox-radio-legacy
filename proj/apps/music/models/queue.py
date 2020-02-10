from datetime import datetime
from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.db import models

from channels.db import database_sync_to_async

from proj.apps.music.models.managers import QueueManager
from proj.apps.music.models.querysets import QueueQuerySet

from proj.core.models import BaseModel


class Queue(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False

    objects = QueueManager.from_queryset(QueueQuerySet)()

    def __str__(self):
        return self.name

    # - - - - - - - - -
    # fields
    # - - - - - - - - -

    stream = models.ForeignKey(
        "music.Stream", related_name="queued", on_delete=models.DO_NOTHING,
    )

    record = models.ForeignKey(
        "music.Record", related_name="queued", on_delete=models.DO_NOTHING,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="queued",
        on_delete=models.DO_NOTHING,
    )

    created_at = models.DateTimeField(default=datetime.now, blank=True)

    played_at = models.DateTimeField(blank=True, null=True)
