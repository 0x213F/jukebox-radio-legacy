
import json

from datetime import datetime

from proj.apps.utils import broadcast_message
from proj.core.models.managers import BaseManager

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


class ShowingManager(BaseManager):
    '''
    Django Manager used to manage Showing objects.
    '''

    def serialize(self, showing):
        showtime_actual_str = (
            showing.showtime_actual.isoformat() if showing.showtime_actual
            else None
        )
        return {
            'uuid': showing.uuid,
            'status': showing.status,
            'showtime_actual': showtime_actual_str,
            'showtime_scheduled': showing.showtime_scheduled.isoformat(),
            'album': {
                'art': showing.album.art,
                'title': showing.album.title,
                'artist': {
                    'full_name': showing.album.artist.full_name,
                }
            }
        }

    def change_status(self, showing, status):
        now = datetime.now()
        showing.showtime_actual = now
        showing.status = status
        showing.save()
        now_str = now.isoformat()
        async_to_sync(channel_layer.group_send)(
            showing.chat_room,
            {
                'type': 'broadcast',
                'spotify': {
                    'context_uri': showing.album.spotify_uri,
                },
                'text': json.dumps({
                    'source': {
                        'type': 'system',
                        'display_name': None,
                        'uuid': None,
                    },
                    'data': {
                        'created_at': now_str,
                        'status': status,
                        'text': None,
                    }
                }),
            }
        )
