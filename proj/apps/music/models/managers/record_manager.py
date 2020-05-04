import uuid
from django.apps import apps
from boto3 import session

import io
import os.path

from django.conf import settings
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

            'storage_id': record.storage_id,
            'storage_filename': record.storage_filename,
            'storage_name': record.storage_name,
            'storage_duration_ms': record.storage_duration_ms,
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


    def create_from_file(self, file):
        Record = apps.get_model('music', 'Record')
        Track = apps.get_model('music', 'Track')
        TrackListing = apps.get_model('music', 'TrackListing')

        session2 = session.Session()
        client = session2.client('s3',
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=f'https://{settings.AWS_S3_REGION_NAME}.digitaloceanspaces.com',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        extension = os.path.splitext(file.name)[1] or '.wav'
        storage_id = str(uuid.uuid4())
        storage_filename = f'uploads/{storage_id}{extension}'

        print(storage_filename)

        client.upload_fileobj(file, 'jukebox-radio-space', storage_filename, ExtraArgs={'ACL': 'public-read'})

        from mutagen.mp3 import MP3

        try:
            audio = MP3(file)
            storage_duration_ms = audio.info.length * 1000
        except Exception:
            import wave
            import contextlib
            fname = '/tmp/test.wav'
            with contextlib.closing(file) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                storage_duration_ms = frames / float(rate)
                print(storage_duration_ms)

        print(storage_duration_ms)
        record = Record.objects.create(
            storage_id=storage_id,
            storage_filename=storage_filename,
            storage_name=file.name,
            storage_duration_ms=storage_duration_ms,
        )

        return record
