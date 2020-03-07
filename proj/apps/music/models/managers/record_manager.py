import json
import requests

import urllib.parse as urlparse
from urllib.parse import urlencode

from datetime import datetime
from datetime import timedelta

from proj.apps.utils import broadcast_message
from proj.core.models.managers import BaseManager
from proj.core.resources import Spotify

from django.apps import apps
from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


class RecordManager(BaseManager):
    """
    Django Manager used to manage Record objects.
    """

    def can_add_track(self, record, track_duration_ms):
        new_duration_ms = record.duration_ms + track_duration_ms
        max_duration_ms = 25 * 60 * 1000
        return new_duration_ms <= max_duration_ms

    def serialize(self, record):
        return {
            "id": record.id,
            "name": record.name,
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
            name=record_name,
            user=user,
            spotify_uri=uri,
            spotify_img=img,
        )

        TrackListing.objects.add_to_record(record, tracks)

        return record
