from proj.core.models.managers import BaseManager
from proj.core.resources import Spotify


class TrackManager(BaseManager):
    '''
    Django Manager used to manage Track objects.
    '''

    def serialize(self, track):
        '''
        Make a Track object JSON serializable.
        '''
        if not track:
            return None
        return {
            'spotify_name': track.spotify_name,
            'spotify_uri': track.spotify_uri,
        }

    def get_or_create_from_uri(self, spotify_uri, user=None):
        Track = self.model
        try:
            return Track.objects.get(spotify_uri=spotify_uri)
        except Track.DoesNotExist:
            pass
        spotify = Spotify(user)
        track_info = spotify.get_track_info(spotify_uri)
        return Track.objects.create(spotify_uri=spotify_uri, **track_info)

    def bulk_create_from_album_info(self, album_info):
        '''
        Bulk create tracks given a list of track data
        '''
        Track = self.model

        # don't re-create tracks that already exist
        spotify_uris = [i['spotify_uri'] for i in album_info]
        tracks_from_db = Track.objects.filter(spotify_uri__in=spotify_uris)
        existing_spotify_uris = tracks_from_db.values_list('spotify_uri', flat=True)

        tracks = []
        for info in album_info:
            if info['spotify_uri'] in existing_spotify_uris:
                continue
            track = Track(**info)
            tracks.append(track)

        Track.objects.bulk_create(tracks)

        return tracks_from_db
