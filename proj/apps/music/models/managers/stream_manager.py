from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from datetime import timedelta

from django.apps import apps

from proj.apps.music import tasks
from proj.core.models.managers import BaseManager


channel_layer = get_channel_layer()


class StreamManager(BaseManager):
    '''
    Django Manager used to manage Stream objects.
    '''

    def serialize(self, stream, active_users=None):
        '''
        Make a Stream object JSON serializable.
        '''
        if not stream:
            return None

        user_count = 0
        if active_users:
            user_count = active_users.count()

        played_at = None
        if stream.played_at:
            played_at = stream.played_at.isoformat()\

        paused_at = None
        if stream.paused_at:
            paused_at = stream.paused_at.isoformat()

        record_terminates_at = None
        if stream.record_terminates_at:
            record_terminates_at = stream.record_terminates_at.isoformat()

        return {
            'uuid': str(stream.uuid),
            'unique_custom_id': stream.unique_custom_id,
            'name': stream.title,
            'status': stream.status,
            'tags': stream.tags,
            'owner_name': stream.owner_name,
            'user_count': user_count,
            'played_at': played_at,
            'paused_at': paused_at,
            'record_terminates_at': record_terminates_at,
        }

    def spin(self, queue, stream, first_spin=False):
        '''
        Spin the record.
        '''
        QueueListing = apps.get_model('music', 'QueueListing')
        Stream = apps.get_model('music', 'Stream')

        if not queue:
            stream.current_queue = None
            stream.record_terminates_at = None
            stream.played_at = None
            stream.paused_at = datetime.now()
            stream.save()
            async_to_sync(channel_layer.group_send)(
                stream.chat_room, {'type': 'sync_playback'},
            )
            return

        record = queue.record

        now = datetime.now()
        if not stream.record_terminates_at:
            # The base case where we play something to start playback.
            spin_at = now + timedelta(seconds=3)
        elif now < stream.record_terminates_at.replace(tzinfo=None):
            # The likely case where we play something that was queued up.
            spin_at = stream.record_terminates_at.replace(tzinfo=None)
        else:
            # The error case where we do "catch up." If we encounter this case,
            # it's likely that the celery queue has gotten backed up.
            spin_at = now

        stream.status = Stream.STATUS_ACTIVATED
        stream.current_queue = queue
        stream.record_begun_at = spin_at
        if record.youtube_id:
            record_length = record.youtube_duration_ms
        else:
            record_length = record.tracks_through.all().duration()
        stream.record_terminates_at = spin_at + timedelta(milliseconds=record_length)
        stream.played_at = spin_at
        stream.paused_at = None
        stream.save()

        played_at = spin_at
        qls = []
        for track_listing in record.tracks_through.all().order_by('number'):
            duration = track_listing.track.spotify_duration_ms
            ql = QueueListing(
                queue=queue,
                track_listing=track_listing,
                start_at_ms=0,
                end_at_ms=duration,
                played_at=played_at,
            )
            qls.append(ql)
            played_at += timedelta(milliseconds=duration)

        QueueListing.objects.bulk_create(qls)

        async_to_sync(channel_layer.group_send)(
            stream.chat_room, {'type': 'sync_playback'},
        )

        next_play_time = stream.record_terminates_at.replace(tzinfo=None) - timedelta(seconds=3)
        tasks.schedule_spin.apply_async(eta=next_play_time, args=[stream.id])

        queue.played_at = now
        queue.save()

        return stream, queue
