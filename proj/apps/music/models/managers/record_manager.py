from django.apps import apps

from proj.core.models.managers import BaseManager
from proj.core.resources import Spotify
from proj.core.resources import YouTube


class RecordManager(BaseManager):
    '''
    Django Manager used to manage Record objects.
    '''

    def serialize(self, record):
        '''
        Make a Queue object JSON serializable.
        '''
        return {
            'spotify_uri': record.spotify_uri,
            'spotify_name': record.spotify_name,
            'spotify_duration_ms': record.spotify_duration_ms,
            'spotify_img': record.spotify_img,
            'youtube_id': record.youtube_id,
            'youtube_name': record.youtube_name,
            'youtube_duration_ms': record.youtube_duration_ms,
            'youtube_img_high': record.youtube_img_high,
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
            spotify_name=record_name, spotify_uri=uri, spotify_img=img,
        )

        TrackListing.objects.add_to_record(record, tracks)

        return record

    def get_or_create_from_youtube_id(self, youtube_id):
        Record = apps.get_model('music', 'Record')
        Track = apps.get_model('music', 'Track')
        TrackListing = apps.get_model('music', 'TrackListing')
        try:
            # assume the record is finalized
            return Record.objects.get(youtube_id=youtube_id)
        except Record.DoesNotExist:
            pass

        video_info = YouTube.get_info(youtube_id)

        record = Record.objects.create(
            youtube_id=video_info['youtube_id'],
            youtube_name=video_info['youtube_name'],
            youtube_duration_ms=video_info['youtube_duration_ms'],
            youtube_img_high=video_info['youtube_img_high'],
        )

        return record
