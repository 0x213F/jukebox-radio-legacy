import requests
from urllib.parse import urlparse
from cryptography.fernet import Fernet

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class Spotify(object):

    def __init__(self, user):
        self.user = user
        self._token = None

    @classmethod
    def get_spotify_authorization_uri(cls, request, source):
        if source not in SOURCE_CHOICES:
            raise Exception("Invalid source choice")
        current_site = get_current_site(request)
        params = {
            "client_id": "890e3c32aaac4e0fa3dd5cfc22835f11",
            "response_type": "code",
            "redirect_uri": f"http://{current_site}/connect?source={source}",
            "scope": "streaming%20app-remote-control%20user-modify-playback-state%20user-read-currently-playing%20user-read-playback-state",
        }
        params_str = urlencode(params)
        return f"https://accounts.spotify.com/authorize?{params_str}"

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


    def get_playlist_info(self, spotify_uri):
        spotify_id = spotify_uri[17:]
        response = requests.get(
            f'https://api.spotify.com/v1/playlists/{spotify_id}',
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        return [
            {
                'spotify_uri': track['track']['uri'],
                'spotify_duration_ms': track['track']['duration_ms'],
                'spotify_name': track['track']['name'],
            } for track in response_json['tracks']['items']
        ]
