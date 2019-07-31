
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

    # - - - - - - -
    # config model
    # - - - - - - -

    STATUS_SCHEDULED = 'scheduled'
    STATUS_ACTIVATED = 'activated'
    STATUS_COMPLETED = 'completed'
    STATUS_TERMINATED = 'terminated'

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_ACTIVATED, 'Activated'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_TERMINATED, 'Terminated'),
    ]

    class Meta:
        abstract = False

    objects = ShowingManager.from_queryset(ShowingQuerySet)()

    def __str__(self):
        return f'[{self.status.upper()}] {self.album}'

    # - - - -
    # fields
    # - - - -

    album = models.ForeignKey(
        'music.Album',
        related_name='albums',
        on_delete=models.DO_NOTHING,
    )
    status = models.CharField(editable=False, max_length=128, default=STATUS_SCHEDULED)

    actual_showtime = models.DateTimeField(null=True, blank=False)
    scheduled_showtime = models.DateTimeField()

    @property
    def chat_room(self):
        return f'showing-{self.id}'
