import json
import requests

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

        # record.is_playing = True
        # record.played_at = now
        # record.save()
        #
        # record.showing.showtime_actual = now
        # record.showing.save()

        data = record.tracks
        spotify_ids = [uri[14:] for uri in data['uris']]
        get_tracks_data = {'ids': spotify_ids}

        sat = 'BQCowU4TA-KE0kwnMNbxcGV1FAgQr4yliFG0APkW-hmrWLasoMqnUNF8c1CVfFUKpjAARKdqkau3S8rO5AsBleHiZjMqRQgSl-82q8r-n6IMOdnhppMBFt0werrR1MEi95-vEqI6lsX71OoIoeE7qCcWUJw'
        response = requests.get(
            'https://api.spotify.com/v1/tracks',
            data=get_tracks_data,
            headers={
                'Authorization': f'Bearer {sat}',
                'Content-Type': 'application/json',
            },
        )
        print(response.json)

        async_to_sync(channel_layer.group_send)(
            record.showing.chat_room,
            {
                'type': 'broadcast',
                'playback': {
                    'action': 'play',
                    'data': data,
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
