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
    pass

    def serialize(self, queue):
        return {
            'id': queue.id,
            'stream_uuid': queue.stream.uuid,
            'record_id': queue.record_id,
            'record_name': queue.record.name,
            'record_spotify_img': queue.record.spotify_img,
            'created_at': queue.created_at.isoformat(),
        }
