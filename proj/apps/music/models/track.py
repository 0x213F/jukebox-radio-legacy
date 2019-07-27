
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

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = TrackManager.from_queryset(TrackQuerySet)()

    # - - - -
    # fields
    # - - - -

    number = models.PositiveIntegerField()

    track_name = models.CharField(editable=False, max_length=128)

    album = models.ForeignKey(
        'music.Artist',
        related_name='tracks',
        on_delete=models.DO_NOTHING,
    )

    runtime = models.FloatField()
