
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

    objects = TrackManager.from_queryset(TrackQuerySet)()

    def __str__(self):
        return f'<track id="{self.id}">'

    # - - - -
    # fields
    # - - - -

    spotify_uri = models.CharField(max_length=36)  # TODO make unique
    spotify_name = models.CharField(max_length=64)
    spotify_duration_ms = models.PositiveIntegerField()
