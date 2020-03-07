from proj.core.models.managers import BaseManager


class TrackListingManager(BaseManager):
    """
    Django Manager used to manage Track objects.
    """

    def serialize(self, tracklisting):
        return {
            "track": {
                "spotify_name": tracklisting.track.spotify_name,
                "spotify_uri": tracklisting.track.spotify_uri,
                "spotify_duration_ms": tracklisting.track.spotify_duration_ms,
            }
        }

    def add_to_record(self, record, tracks):
        TrackListing = self.model
        tls = []
        number = 1
        for track in tracks:
            tl = TrackListing(
                record=record, track=track, number=number,
            )
            tls.append(tl)
            number += 1
        TrackListing.objects.bulk_create(tls)
