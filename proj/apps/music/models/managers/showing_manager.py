
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
        return {
            'uuid': showing.uuid,
            'status': showing.status,
            'showtime_actual': showing.showtime_actual,
            'showtime_scheduled': showing.showtime_scheduled,
            'album': {
                'art': showing.album.art,
                'title': showing.album.title,
                'artist': {
                    'full_name': showing.album.artist.full_name,
                }
            }
        }

    def update(self, *, status=None):
        now = datetime.now()
        super().update(
            actual_showtime=now,
            status=status,
        )
        now_str = now.isoformat()
        for showing in queryset:
            async_to_sync(channel_layer.group_send)(
                showing.chat_room,
                broadcast_message({
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
                })
            )
