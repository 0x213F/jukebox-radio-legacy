
import random
import uuid

from datetime import datetime
from datetime import timezone

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.music.models.managers import ShowingManager
from proj.apps.music.models.querysets import ShowingQuerySet

from proj.core.models import BaseModel


class Showing(BaseModel):

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = ShowingManager.from_queryset(ShowingQuerySet)()

    STATUS_SCHEDULED = 'scheduled'
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETE = 'complete'
    STATUS_TERMINATED = 'terminated'

    # - - - -
    # fields
    # - - - -

    album = models.ForeignKey(
        'music.Album',
        related_name='albums',
        on_delete=models.DO_NOTHING,
    )
    status = models.CharField(editable=False, max_length=128, default=STATUS_SCHEDULED)
    scheduled_showtime = models.DateTimeField()
    actual_showtime = models.DateTimeField(null=True, blank=False)

    def __str__(self):
        if self.status == self.STATUS_SCHEDULED:
            now = datetime.now(tz=timezone.utc)
            starts_in_minutes = int((self.showtime - now).total_seconds() / 60)
            return f'{self.album} starts in {starts_in_minutes} minutes.'
        else:
            return f'[{self.status.upper()}] {self.album}'
