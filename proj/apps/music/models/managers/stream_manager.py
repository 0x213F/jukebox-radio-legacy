from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from datetime import timedelta

from django.apps import apps
from django.db.models import Sum

from proj.apps.music import tasks
from proj.core.models.managers import BaseManager


channel_layer = get_channel_layer()


class StreamManager(BaseManager):
    '''
    Django Manager used to manage Stream objects.
    '''

    def serialize(self, stream, active_users=None):
        if not stream:
            return None

        user_count = 0
        if active_users:
            user_count = active_users.count()

        return {
            'uuid': str(stream.uuid),
            'unique_custom_id': stream.unique_custom_id,
            'name': stream.title,
            'status': stream.status,
            'tags': stream.tags,
            'owner_name': stream.owner_name,
            'user_count': user_count,
        }

    def spin(self, queue, stream):
        '''
        Spin the record.
        '''
        Stream = apps.get_model('music', 'Stream')

        record = queue.record

        current_tracklisting = (
            record.tracks_through.select_related('track').order_by('number').first()
        )
        stream.current_tracklisting = current_tracklisting
        now = datetime.now()
        stream.last_status_change_at = now
        stream.status = Stream.STATUS_ACTIVATED
        stream.tracklisting_begun_at = now
        stream.tracklisting_terminates_at = now + timedelta(
            milliseconds=current_tracklisting.track.spotify_duration_ms
        )
        stream.paused_at = None
        stream.current_record = record
        record_length = record.tracks_through.all().aggregate(
            Sum('track__spotify_duration_ms')
        )['track__spotify_duration_ms__sum']
        stream.record_terminates_at = now + timedelta(milliseconds=record_length)
        stream.save()

        async_to_sync(channel_layer.group_send)(
            stream.chat_room, {'type': 'sync_playback',},
        )

        next_play_time = stream.record_terminates_at.replace(tzinfo=None)
        tasks.schedule_spin.apply_async(eta=next_play_time, args=[stream.id])

        queue.played_at = now
        queue.save()

        return stream, queue
