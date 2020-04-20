from channels.layers import get_channel_layer
from datetime import timedelta
from datetime import datetime

from django.apps import apps
from proj.core.models.managers import BaseManager


channel_layer = get_channel_layer()


class QueueManager(BaseManager):
    '''
    Django Manager used to manage Queue objects.
    '''

    def create(self, *, record=None, stream=None, user=None):
        Queue = apps.get_model('music', 'Queue')

        if not record or not stream or not user:
            raise ValueError('Must supply record, stream, and user')

        queue = Queue.objects.filter(stream=stream).order_by('created_at').last()
        if not queue:
            scheduled_at = datetime.now()
        else:
            scheduled_at = queue.scheduled_at + timedelta(milliseconds=record.duration_ms)

        return super().create(
            record=record,
            stream=stream,
            user=user,
            scheduled_at=scheduled_at,
        )

    def serialize(self, queue, prev_end_dt=None):
        '''
        Make a Queue object JSON serializable.
        '''
        Record = apps.get_model('music', 'Record')
        return {
            'id': queue.id,
            'stream_uuid': str(queue.stream.uuid),
            'record': Record.objects.serialize(queue.record),
            'created_at': queue.created_at.isoformat(),
            'scheduled_at': queue.scheduled_at.isoformat(),
        }
