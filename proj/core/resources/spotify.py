import requests
from urllib.parse import urlparse
from cryptography.fernet import Fernet

from django.conf import settings


class Spotify(object):

    def __init__(self, user):
        self.user = user
        self._token = None

    @property
    def token(self):
        if not self._token:
            self._token = Fernet(settings.DATABASE_ENCRYPTION_KEY).decrypt(
                self.user.profile.spotify_access_token.encode("utf-8")
            ).decode("utf-8")
        return self._token

    def search_library(self, query, type):
        data = {
            'q': query,
            'type': type,
        }
        response = requests.get(
            f'https://api.spotify.com/v1/search',
            params=data,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        if type == 'album':
            return [
                {
                    'artist': ', '.join([a['name'] for a in data['artists']]),
                    'record_name': data['name'],
                    'uri': data['uri'],
                    'record_img_640': data['images'][0]['url'],
                } for data in response_json['albums']['items']
            ]
        elif type == 'playlist':
            return [
                {
                    'record_name': data['name'],
                    'uri': data['uri'],
                    'record_img_640': data['images'][0]['url'],
                } for data in response_json['playlists']['items']
            ]
        else:
            return [
                {
                    'artist': ', '.join([a['name'] for a in data['artists']]),
                    'record_name': data['name'],
                    'uri': data['uri'],
                    'record_img_640': data['album']['images'][0]['url'],
                } for data in response_json['tracks']['items']
            ]

    def get_track_info(self, spotify_uri):
        spotify_id = spotify_uri[14:]
        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{spotify_id}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        return {
            'spotify_duration_ms': response_json["duration_ms"],
            'spotify_name': response_json["name"][:32],
        }

    def get_album_info(self, spotify_uri):
        spotify_id = spotify_uri[14:]
        response = requests.get(
            f'https://api.spotify.com/v1/albums/{spotify_id}/tracks',
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        return [
            {
                'spotify_uri': track['uri'],
                'spotify_duration_ms': track['duration_ms'],
                'spotify_name': track['name'],
            } for track in response_json['items']
        ]
