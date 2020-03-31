import json

from datetime import datetime

from django.apps import apps

from proj.core.models.managers import BaseManager

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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


class StreamManager(BaseManager):
    """
    Django Manager used to manage Stream objects.
    """

    def serialize(self, stream, active_users=None):
        if not stream:
            return None

        user_count = 0
        if active_users:
            user_count=active_users.count()

        return {
            "uuid": str(stream.uuid),
            "unique_custom_id": stream.unique_custom_id,
            "name": stream.title,
            "status": stream.status,
            "tags": stream.tags,
            "owner_name": stream.owner_name,
            "user_count": user_count,
        }

    def spin(self, record, stream):
        """
        Spin the record.
        """
        Stream = apps.get_model('music', 'Stream')
        Record = apps.get_model('music', 'Record')
        Ticket = apps.get_model('music', 'Ticket')
        Comment = apps.get_model('music', 'Comment')

        now = datetime.now()
        now_str = now.isoformat()

        track_timestamp = now
        for tl in record.tracks_through.select_related('track').all().order_by('number'):
            track = tl.track
            Comment.objects.create(
                created_at=track_timestamp,
                status=Comment.STATUS_START,
                text=None,
                commenter=None,
                stream=stream,
                track=track,
                record=record,
                commenter_ticket=None,
            )
            track_timestamp += timedelta(milliseconds=track.spotify_duration_ms)

        stream.current_record = record
        stream.record_terminates_at = track_timestamp
        stream.save()

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_SPIN,
            text=None,
            commenter=None,
            stream=stream,
            track=None,
            record=record,
            commenter_ticket=None,
        )

        uris = list(
            record.tracks_through.all()
            .order_by("number")
            .values_list("track__spotify_uri", flat=True)
        )

        async_to_sync(channel_layer.group_send)(
            stream.chat_room,
            {
                "type": "sync_playback",
            },
        )

    def play(self, record):
        """
        Play the record sitting in a paused state.
        """
        now = datetime.now()

        record.is_playing = True
        record.save()

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_PLAY,
            text=None,
            commenter=master_user,
            stream=stream,
            track=None,
            commenter_ticket=active_ticket,
        )

        async_to_sync(channel_layer.group_send)(
            record.stream.chat_room,
            {
                "type": "broadcast",
                "playback": {"action": "play", "data": None,},
                "text": json.dumps(
                    {
                        "source": {
                            "type": "system",
                            "display_name": None,
                            "uuid": None,
                        },
                        "data": {"created_at": None, "status": None, "text": None,},
                    }
                ),
            },
        )

    def pause(self, record):
        """
        Pause the record currently playing.
        """
        now = datetime.now()

        record.is_playing = False
        record.save()

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_PAUSE,
            text=None,
            commenter=master_user,
            stream=stream,
            track=None,
            commenter_ticket=active_ticket,
        )

        async_to_sync(channel_layer.group_send)(
            record.stream.chat_room,
            {
                "type": "broadcast",
                "playback": {"action": "pause", "data": None,},
                "text": json.dumps(
                    {
                        "source": {
                            "type": "system",
                            "display_name": None,
                            "uuid": None,
                        },
                        "data": {"created_at": None, "status": None, "text": None,},
                    }
                ),
            },
        )

    def stop(self, record, stream):
        """
        Stop the record currently spinning.
        """

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_STOP,
            text=None,
            commenter=master_user,
            stream=stream,
            track=None,
            commenter_ticket=active_ticket,
        )

        Comment.objects.filter(
            created_at__gte=now,
            status=Comment.STATUS_START,
            text=None,
            commenter=None,
            stream=stream,
            track=None,
            commenter_ticket=None,
        ).delete()

        # TODO pause ongoing track
