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
from django.db.models import Sum

from proj.apps.music import tasks

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

    def spin(self, queue, stream):
        """
        Spin the record.
        """
        Stream = apps.get_model('music', 'Stream')
        Record = apps.get_model('music', 'Record')
        Ticket = apps.get_model('music', 'Ticket')
        Comment = apps.get_model('music', 'Comment')

        record = queue.record

        current_tracklisting = record.tracks_through.select_related('track').order_by('number').first()
        stream.current_tracklisting = current_tracklisting
        now = datetime.now()
        stream.last_status_change_at = now
        stream.status = Stream.STATUS_ACTIVATED
        stream.tracklisting_begun_at = now
        stream.tracklisting_terminates_at = now + timedelta(milliseconds=current_tracklisting.track.spotify_duration_ms)
        stream.paused_at = None
        stream.current_record = record
        record_length = (
            record.tracks_through.all()
            .aggregate(Sum('track__spotify_duration_ms'))
            ['track__spotify_duration_ms__sum']
        )
        stream.record_terminates_at = now + timedelta(milliseconds=record_length)
        stream.save()

        async_to_sync(channel_layer.group_send)(
            stream.chat_room,
            {
                "type": "sync_playback",
            },
        )

        next_play_time = stream.record_terminates_at.replace(tzinfo=None)
        tasks.schedule_spin.apply_async(
            eta=next_play_time, args=[stream.id]
        )

        queue.played_at = now
        queue.save()

        return stream, queue

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
