from django.db import models

from proj.apps.music.models.managers import TrackManager
from proj.apps.music.models.querysets import TrackQuerySet
from proj.core.models import BaseModel


class Track(BaseModel):

    # - - - - - - -
    # config model |
    # - - - - - - -

    class Meta:
        abstract = False

    objects = TrackManager.from_queryset(TrackQuerySet)()

    def __str__(self):
        return self.spotify_name

    # - - - -
    # fields |
    # - - - -

    spotify_uri = models.CharField(max_length=64)  # TODO make unique
    spotify_name = models.CharField(max_length=256)
    spotify_duration_ms = models.PositiveIntegerField()
