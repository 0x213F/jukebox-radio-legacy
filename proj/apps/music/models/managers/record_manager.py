import json
import requests

import urllib.parse as urlparse
from urllib.parse import urlencode

from datetime import datetime
from datetime import timedelta

from proj.apps.utils import broadcast_message
from proj.core.models.managers import BaseManager

from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


class RecordManager(BaseManager):
    '''
    Django Manager used to manage Record objects.
    '''

    def can_add_track(self, record, track_duration_ms):
        new_duration_ms = record.duration_ms + track_duration_ms
        max_duration_ms = 25 * 60 * 1000
        return new_duration_ms <= max_duration_ms
