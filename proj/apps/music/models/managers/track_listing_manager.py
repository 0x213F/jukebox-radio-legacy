from django.apps import apps

from proj.core.models.managers import BaseManager


class TrackListingManager(BaseManager):
    """
    Django Manager used to manage TrackListing objects.
    """

    def serialize(self, tracklisting):
        """
        Make a TrackListing object JSON serializable.
        """
        Track = apps.get_model("music", "Track")
        return {
            "track": Track.objects.serialize(tracklisting.track),
        }

    def add_to_record(self, record, tracks):
        """
        Add some tracks to a record.

        NOTE: we assume that the record has no tracks.
        """
        TrackListing = self.model
        tls = []

        number = 1
        for track in tracks:
            tl = TrackListing(record=record, track=track, number=number,)
            tls.append(tl)
            number += 1
        TrackListing.objects.bulk_create(tls)
