from django.apps import apps

from proj.core.models.managers import BaseManager
from proj.core.resources import Spotify


class RecordManager(BaseManager):
    '''
    Django Manager used to manage Record objects.
    '''

    def serialize(self, record):
        '''
        Make a Queue object JSON serializable.
        '''
        return {
            'name': record.name,
            'img': record.spotify_img,
        }

    def get_or_create_from_uri(self, uri, record_name, img, user=None):
        Record = apps.get_model('music', 'Record')
        Track = apps.get_model('music', 'Track')
        TrackListing = apps.get_model('music', 'TrackListing')
        try:
            # assume the record is finalized
            return Record.objects.get(spotify_uri=uri)
        except Record.DoesNotExist:
            pass
        if 'track' in uri:
            tracks = [Track.objects.get_or_create_from_uri(uri, user=user)]
        elif 'album' in uri:
            spotify = Spotify(user)
            album_info = spotify.get_album_info(uri)
            tracks = Track.objects.bulk_create_from_album_info(album_info)
        elif 'playlist' in uri:
            spotify = Spotify(user)
            album_info = spotify.get_playlist_info(uri)
            tracks = Track.objects.bulk_create_from_album_info(album_info)

        record = Record.objects.create(
            name=record_name, spotify_uri=uri, spotify_img=img,
        )

        TrackListing.objects.add_to_record(record, tracks)

        return record
