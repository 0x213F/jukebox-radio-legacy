from datetime import datetime

from django.apps import apps

from proj.core.models.managers import BaseManager
from proj.core.resources import dates


class QueueListingManager(BaseManager):
    """
    Django Manager used to manage QueueListing objects.
    """

    def serialize(self, queuelisting):
        """
        Make a QueueListing object JSON serializable.
        """
        TrackListing = apps.get_model("music", "TrackListing")
        return {
            "start_at_ms": queuelisting.start_at_ms,
            "end_at_ms": queuelisting.end_at_ms,
            "played_at": dates.unix_time(queuelisting.played_at),
            "paused_at": queuelisting.played_at.isoformat(),
            "tracklisting": TrackListing.objects.serialize(queuelisting.track_listing),
        }
