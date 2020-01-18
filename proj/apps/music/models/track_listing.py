import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.music.models.managers import TrackListingManager
from proj.apps.music.models.querysets import TrackListingQuerySet

from proj.core.models import BaseModel


class TrackListing(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False
        unique_together = ["track", "record", "number"]

    objects = TrackListingManager.from_queryset(TrackListingQuerySet)()

    def __str__(self):
        return f"[{self.number}] {self.record}: {self.track}"

    # - - - -
    # fields
    # - - - -

    track = models.ForeignKey(
        "music.Track", related_name="records_through", on_delete=models.DO_NOTHING,
    )

    record = models.ForeignKey(
        "music.Record", related_name="tracks_through", on_delete=models.CASCADE,
    )

    number = models.PositiveIntegerField()
