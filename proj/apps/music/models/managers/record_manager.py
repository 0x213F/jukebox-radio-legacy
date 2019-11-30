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

    def spin(self, record):
        '''

        '''
        from proj.apps.music.models import Ticket
        from proj.apps.music.models import Comment

        now = datetime.now()
        now_str = now.isoformat()
        master_user = User.objects.get(email__iexact='josh@schultheiss.io')

        # record.is_playing = True
        # record.played_at = now
        # record.save()
        #
        # record.showing.showtime_actual = now
        # record.showing.save()

        showing = record.showing
        active_ticket = Ticket.objects.get(
            holder=master_user,
            showing__uuid=showing.uuid,
        )
        track_timestamp = now
        for track in record.tracks.all().order_by('value'):
            comment = Comment.objects.create(
                created_at=track_timestamp,
                status='play',
                text=None,
                commenter=master_user,
                showing=showing,
                track=track,
                commenter_ticket=active_ticket,
            )
            track_timestamp += timedelta(milliseconds=track.spotify_duration_ms)

        uris = list(
            record.tracks.all().order_by('value')
            .values_list('spotify_uri', flat=True)
        )
        async_to_sync(channel_layer.group_send)(
            record.showing.chat_room,
            {
                'type': 'broadcast',
                'playback': {
                    'action': 'play',
                    'data': {'uris': uris},
                },
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

        async_to_sync(channel_layer.group_send)(
            record.showing.chat_room,
            {
                'type': 'broadcast',
                'playback': {
                    'action': 'play',
                    'data': None,
                },
                'text': json.dumps({
                    'source': {
                        'type': 'system',
                        'display_name': None,
                        'uuid': None,
                    },
                    'data': {
                        'created_at': None,
                        'status': None,
                        'text': None,
                    }
                }),
            }
        )

    def pause(self, record):
        '''

        '''
        record.is_playing = False
        record.save()

        async_to_sync(channel_layer.group_send)(
            record.showing.chat_room,
            {
                'type': 'broadcast',
                'playback': {
                    'action': 'pause',
                    'data': None,
                },
                'text': json.dumps({
                    'source': {
                        'type': 'system',
                        'display_name': None,
                        'uuid': None,
                    },
                    'data': {
                        'created_at': None,
                        'status': None,
                        'text': None,
                    }
                }),
            }
        )
