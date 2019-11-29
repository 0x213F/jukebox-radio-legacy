import json

from datetime import datetime

from proj.apps.utils import broadcast_message
from proj.core.models.managers import BaseManager

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


class RecordManager(BaseManager):
    '''
    Django Manager used to manage Record objects.
    '''

    def spin(self, record):
        '''

        '''
        now = datetime.now()
        now_str = now.isoformat()

        record.is_playing = True
        record.played_at = now
        record.save()

        record.showing.showtime_actual = now
        record.showing.save()
        async_to_sync(channel_layer.group_send)(
            record.showing.chat_room,
            {
                'type': 'broadcast',
                'tracks': record.tracks,
                'text': json.dumps({
                    'source': {
                        'type': 'system',
                        'display_name': None,
                        'uuid': None,
                    },
                    'data': {
                        'created_at': now_str,
                        'status': None,
                        'text': None,
                    }
                }),
            }
        )

    def play(self, record):
        '''

        '''
        record.is_playing = True
        record.save()

    def pause(self, record):
        '''

        '''
        record.is_playing = False
        record.save()
