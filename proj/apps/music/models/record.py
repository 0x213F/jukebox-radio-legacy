
from datetime import timedelta

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.apps import apps

from proj.apps.music.models.managers import RecordManager
from proj.apps.music.models.querysets import RecordQuerySet

from proj.core.models import BaseModel


class Record(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False

    objects = RecordManager.from_queryset(RecordQuerySet)()

    def __str__(self):
        return self.name

    # - - - - - - - - -
    # fields
    # - - - - - - - - -

    name = models.CharField(max_length=128)

    is_playing = models.BooleanField(default=False)

    tracks = models.ManyToManyField('music.Track', through='music.TrackListing')

    @property
    def duration_ms(self):
        TrackListing = apps.get_model('music.TrackListing')
        track_durations_ms = (
            TrackListing
            .objects
            .filter(record=self)
            .order_by('number')
            .values_list('track__spotify_duration_ms', flat=True)
        )
        return sum(track_durations_ms)
