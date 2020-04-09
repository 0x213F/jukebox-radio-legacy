from channels.layers import get_channel_layer
from datetime import timedelta

from proj.core.models.managers import BaseManager


channel_layer = get_channel_layer()


class QueueManager(BaseManager):
    '''
    Django Manager used to manage Queue objects.
    '''

    def serialize(self, queue, prev_end_dt=None):
        '''
        Make a Queue object JSON serializable.
        '''
        will_play_at = prev_end_dt.isoformat() if prev_end_dt else None
        next_play_at = (
            prev_end_dt + timedelta(milliseconds=queue.record.duration_ms)
            if prev_end_dt
            else None
        )
        return (
            {
                'id': queue.id,
                'stream_uuid': queue.stream.uuid,
                'record_id': queue.record_id,
                'record_name': queue.record.name,
                'record_spotify_img': queue.record.spotify_img,
                'created_at': queue.created_at.isoformat(),
                'playing_at': will_play_at,
            },
            next_play_at,
        )

    def serialize_list(self, stream, queue_list):
        '''
        Make a Queue object JSON serializable.
        '''
        arr = []

        end_dt = stream.record_terminates_at
        for queue in queue_list:
            queue_obj, end_dt = self.serialize(queue, prev_end_dt=end_dt)
            arr.append(queue_obj)

        return arr
