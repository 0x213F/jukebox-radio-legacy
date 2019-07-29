
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
        unique_together = ['number', 'album']

    objects = TrackManager.from_queryset(TrackQuerySet)()

    def __str__(self):
        return f'[{self.number}] {self.name}'

    # - - - -
    # fields
    # - - - -

    number = models.PositiveIntegerField()

    name = models.CharField(max_length=128)

    album = models.ForeignKey(
        'music.Album',
        related_name='tracks',
        on_delete=models.DO_NOTHING,
    )

    runtime = models.FloatField()
