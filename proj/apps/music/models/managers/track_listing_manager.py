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
