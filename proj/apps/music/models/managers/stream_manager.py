
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


class StreamManager(BaseManager):
    '''
    Django Manager used to manage Stream objects.
    '''

    def serialize(self, stream):
        if not stream:
            return None
        return {
            'uuid': str(stream.uuid),
            'name': stream.title,
            'status': stream.status,
        }

    def change_status(self, stream, status):
        '''
        '''
        Comment = apps.get_model('music.Comment')
        Record = apps.get_model('music.Record')
        Stream = apps.get_model('music.Stream')
        Track = apps.get_model('music.Track')

        now = datetime.now()
        now_str = now.isoformat()

        stream.status = status
        stream.last_status_change_at = datetime.now()
        stream.save()

        Comment.objects.create(
            status=status,
            text=None,
            commenter=None,
            stream=stream,
            track=None,
            commenter_ticket=None,
        )

        async_to_sync(channel_layer.group_send)(
            stream.chat_room,
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

    def spin(self, record, stream):
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
                stream=stream,
                track=track,
                commenter_ticket=None,
            )
            track_timestamp += timedelta(milliseconds=track.spotify_duration_ms)

        stream.current_record = record
        stream.record_terminates_at = track_timestamp
        stream.save()

        Comment.objects.create(
            created_at=now,
            status=Comment.STATUS_SPIN,
            text=None,
            commenter=None,
            stream=stream,
            track=None,
            record=record,
            commenter_ticket=None,
        )

        uris = list(
            record.tracks_through.all().order_by('number')
            .values_list('track__spotify_uri', flat=True)
        )

        async_to_sync(channel_layer.group_send)(
            stream.chat_room,
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

        for ticket in Ticket.objects.filter(is_subscribed=True, stream=stream):

            most_recent_join = Comment.objects.filter(
                status=Comment.STATUS_JOINED,
                commenter=ticket.holder,
            ).order_by('-created_at').first()

            try:
                assert most_recent_join.stream == stream
            except Exception:
                continue

            most_recent_leave = Comment.objects.filter(
                status=Comment.STATUS_LEFT,
                commenter=ticket.holder,
                stream=stream,
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
            stream=stream,
            track=None,
            commenter_ticket=active_ticket,
        )

        async_to_sync(channel_layer.group_send)(
            record.stream.chat_room,
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
            stream=stream,
            track=None,
            commenter_ticket=active_ticket,
        )

        async_to_sync(channel_layer.group_send)(
            record.stream.chat_room,
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

    def stop(self, record, stream):
        '''
        Stop the record currently spinning.
        '''

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
