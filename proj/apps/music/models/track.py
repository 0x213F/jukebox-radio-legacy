
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.music.models.managers import TrackManager
from proj.apps.music.models.querysets import TrackQuerySet

from proj.core.models import BaseModel


class Track(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False
        unique_together = ['record', 'value', 'spotify_uri']

    objects = TrackManager.from_queryset(TrackQuerySet)()

    def __str__(self):
        return f'[{self.record.id}:{self.value}] {self.spotify_name} {self.spotify_duration_ms}'

    # - - - -
    # fields
    # - - - -

    record = models.ForeignKey(
        'music.Record',
        related_name='tracks',
        on_delete=models.DO_NOTHING,
    )

    value = models.PositiveIntegerField()

    spotify_uri = models.CharField(max_length=36)
    spotify_name = models.CharField(max_length=64)
    spotify_duration_ms = models.PositiveIntegerField()
