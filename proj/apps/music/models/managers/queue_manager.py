import json
import requests

import urllib.parse as urlparse
from urllib.parse import urlencode

from datetime import datetime
from datetime import timedelta

from proj.core.models.managers import BaseManager

from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


class QueueManager(BaseManager):
    """
    Django Manager used to manage Queue objects.
    """

    def serialize(self, queue, prev_end_dt=None):
        playing_at = None if not prev_end_dt else (prev_end_dt + timedelta(milliseconds=queue.record.duration_ms))
        print(playing_at)
        playing_at_val = prev_end_dt.isoformat() if playing_at else None
        return {
            'id': queue.id,
            'stream_uuid': queue.stream.uuid,
            'record_id': queue.record_id,
            'record_name': queue.record.name,
            'record_spotify_img': queue.record.spotify_img,
            'created_at': queue.created_at.isoformat(),
            'playing_at': playing_at_val,
        }, playing_at

    def serialize_list(self, stream, queue_list):
        arr = []

        print(stream.record_terminates_at)
        end_dt = stream.record_terminates_at
        for queue in queue_list:
            queue_obj, end_dt = self.serialize(queue, prev_end_dt=end_dt)
            arr.append(queue_obj)

        return arr
