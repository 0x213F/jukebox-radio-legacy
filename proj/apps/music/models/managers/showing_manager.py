
import json

from datetime import datetime

from django.apps import apps

from proj.apps.utils import broadcast_message
from proj.core.models.managers import BaseManager

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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


class ShowingManager(BaseManager):
    '''
    Django Manager used to manage Showing objects.
    '''

    def serialize(self, showing):
        if not showing:
            return None
        return {
            'uuid': str(showing.uuid),
            'name': showing.title,
            'status': showing.status,
        }

    def change_status(self, showing, status):
        '''
        '''
        Comment = apps.get_model('music.Comment')
        Record = apps.get_model('music.Record')
        Showing = apps.get_model('music.Showing')
        Track = apps.get_model('music.Track')

        now = datetime.now()
        now_str = now.isoformat()

        showing.status = status
        showing.save()

        Comment.objects.create(
            status=status,
            text=None,
            commenter=None,
            showing=showing,
            track=None,
            commenter_ticket=None,
        )

        async_to_sync(channel_layer.group_send)(
            showing.chat_room,
            {
                'type': 'broadcast',
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

    def spin(self, record, showing):
        '''
        Spin the record.
        '''
        from proj.apps.music.models import Ticket
        from proj.apps.music.models import Comment

        now = datetime.now()
        now_str = now.isoformat()

        track_timestamp = now
        for tl in record.tracks_through.all().order_by('number'):
            track = tl.track
            Comment.objects.create(
                created_at=track_timestamp,
                status=Comment.STATUS_START,
                text=None,
                commenter=None,
                showing=showing,
                track=track,
                commenter_ticket=None,
            )
            track_timestamp += timedelta(milliseconds=track.spotify_duration_ms)

        showing.current_record = record
        showing.record_terminates_at = track_timestamp
        showing.save()

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_SPIN,
            text=None,
            commenter=None,
            showing=showing,
            track=None,
            record=record,
            commenter_ticket=None,
        )

        uris = list(
            record.tracks_through.all().order_by('number')
            .values_list('track__spotify_uri', flat=True)
        )

        async_to_sync(channel_layer.group_send)(
            showing.chat_room,
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

        for ticket in Ticket.objects.filter(is_subscribed=True, showing=showing):

            most_recent_join = Comment.objects.filter(
                status=Comment.STATUS_JOINED,
                commenter=ticket.holder,
            ).order_by('-created_at').first()

            try:
                assert most_recent_join.showing == showing
            except Exception:
                continue

            most_recent_leave = Comment.objects.filter(
                status=Comment.STATUS_LEFT,
                commenter=ticket.holder,
                showing=showing,
            ).order_by('-created_at').first()

            if (most_recent_join.created_at and not most_recent_leave) or (most_recent_join.created_at > most_recent_leave.created_at):
                print('USER IS IN CHAT AND SUBSCRIBED')
                continue

            user = ticket.holder
            action = 'play'
            data = json.dumps({'uris': uris})
            sat = user.profile.spotify_access_token
            response = requests.put(
                f'https://api.spotify.com/v1/me/player/{action}',
                data=data,
                headers={
                    'Authorization': f'Bearer {sat}',
                    'Content-Type': 'application/json',
                },
            )

    def play(self, record):
        '''
        Play the record sitting in a paused state.
        '''
        now = datetime.now()

        record.is_playing = True
        record.save()

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_PLAY,
            text=None,
            commenter=master_user,
            showing=showing,
            track=None,
            commenter_ticket=active_ticket,
        )

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
        Pause the record currently playing.
        '''
        now = datetime.now()

        record.is_playing = False
        record.save()

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_PAUSE,
            text=None,
            commenter=master_user,
            showing=showing,
            track=None,
            commenter_ticket=active_ticket,
        )

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

    def stop(self, record, showing):
        '''
        Stop the record currently spinning.
        '''

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_STOP,
            text=None,
            commenter=master_user,
            showing=showing,
            track=None,
            commenter_ticket=active_ticket,
        )

        Comment.objects.filter(
            created_at__gte=now,
            status=Comment.STATUS_START,
            text=None,
            commenter=None,
            showing=showing,
            track=None,
            commenter_ticket=None,
        ).delete()

        # TODO pause ongoing track
