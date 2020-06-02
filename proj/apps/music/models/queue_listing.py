from datetime import datetime

from django.conf import settings
from django.db import models

from proj.apps.music.models.managers import QueueListingManager
from proj.apps.music.models.querysets import QueueListingQuerySet
from proj.core.models import BaseModel


class QueueListing(BaseModel):

    # - - - - - - -
    # config model |
    # - - - - - - -

    class Meta:
        abstract = False

    objects = QueueListingManager.from_queryset(QueueListingQuerySet)()

    def __str__(self):
        return f"{self.queue}: {self.track_listing}"

    # - - - -
    # fields |
    # - - - -

    queue = models.ForeignKey(
        "music.Queue", related_name="queue_listings", on_delete=models.DO_NOTHING,
    )

    # TODO this can be FK to tracks instead
    track_listing = models.ForeignKey(
        "music.Tracklisting",
        related_name="queued_listing",
        on_delete=models.DO_NOTHING,
    )

    start_at_ms = models.PositiveIntegerField()
    end_at_ms = models.PositiveIntegerField()

    played_at = models.DateTimeField(blank=True, null=True)
    paused_at = models.DateTimeField(blank=True, null=True)
