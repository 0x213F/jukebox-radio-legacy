from proj.core.models.managers import BaseManager


class TrackManager(BaseManager):
    """
    Django Manager used to manage Track objects.
    """

    pass

    def serialize(self, track):
        if not track:
            return None
        return {
            "spotify_name": track.spotify_name,
            "spotify_uri": track.spotify_uri,
        }
