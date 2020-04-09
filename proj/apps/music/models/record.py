from django.apps import apps
from django.db import models

from proj.apps.music.models.managers import RecordManager
from proj.apps.music.models.querysets import RecordQuerySet
from proj.core.models import BaseModel


class Record(BaseModel):

    # - - - - - - -
    # config model |
    # - - - - - - -

    class Meta:
        abstract = False

    objects = RecordManager.from_queryset(RecordQuerySet)()

    def __str__(self):
        return self.name

    # - - - -
    # fields |
    # - - - -

    name = models.CharField(max_length=128)

    tracks = models.ManyToManyField('music.Track', through='music.TrackListing')

    spotify_uri = models.CharField(max_length=128)  # TODO make unique
    spotify_name = models.CharField(max_length=128)
    spotify_duration_ms = models.PositiveIntegerField(null=True, blank=True)
    spotify_img = models.CharField(max_length=256)

    @property
    def duration_ms(self):
        TrackListing = apps.get_model('music.TrackListing')
        track_durations_ms = TrackListing.objects.from_record(self).values_list(
            'track__spotify_duration_ms', flat=True
        )
        return sum(track_durations_ms)
