from datetime import datetime

from django.conf import settings
from django.db import models

import uuid as _uuid

from proj.apps.music.models.managers import QueueManager
from proj.apps.music.models.querysets import QueueQuerySet

from proj.core.models import BaseModel


class Queue(BaseModel):

    # - - - - - - -
    # config model |
    # - - - - - - -

    class Meta:
        abstract = False

    objects = QueueManager.from_queryset(QueueQuerySet)()

    def __str__(self):
        return f'[{self.user}] {self.record}'

    # - - - -
    # fields |
    # - - - -

    uuid = models.UUIDField(default=_uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='queued', on_delete=models.DO_NOTHING,
    )

    record = models.ForeignKey(
        'music.Record', related_name='queued', on_delete=models.DO_NOTHING,
    )

    stream = models.ForeignKey(
        'music.Stream', related_name='queued', on_delete=models.DO_NOTHING,
    )

    played_at = models.DateTimeField(blank=True, null=True)

    scheduled_at = models.DateTimeField()
