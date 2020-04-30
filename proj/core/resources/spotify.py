import requests
import requests_async
from urllib.parse import urlparse
from cryptography.fernet import Fernet

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class Spotify(object):
    def __init__(self, user, profile=None, async_mode=False):
        self.user = user
        self.profile = profile
        self._token = None
        self._refresh_token = None
        self._async = async_mode
        self._cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)

    def store_access_token(self, access_token):
        profile = self.profile or self.user.profile
        cipher_spotify_access_token = self._cipher_suite.encrypt(
            access_token.encode("utf-8")
        ).decode("utf-8")
        profile.spotify_access_token = cipher_spotify_access_token
        profile.save()

    def store_refresh_token(self, refresh_token):
        profile = self.profile or self.user.profile
        cipher_spotify_refresh_token = self._cipher_suite.encrypt(
            refresh_token.encode("utf-8")
        ).decode("utf-8")
        profile.spotify_refresh_token = cipher_spotify_refresh_token
        profile.save()

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
            profile = self.profile or self.user.profile
            self._token = self._cipher_suite.decrypt(
                profile.spotify_access_token.encode("utf-8")
            ).decode("utf-8")
        return self._token

    @property
    def refresh_token(self):
        if not self._refresh_token:
            profile = self.profile or self.user.profile
            self._refresh_token = self._cipher_suite.decrypt(
                profile.spotify_refresh_token.encode("utf-8")
            ).decode("utf-8")
        return self._refresh_token

    def search_library(self, query, type):
        data = {
            "q": query,
            "type": type,
        }
        response = requests.get(
            f"https://api.spotify.com/v1/search",
            params=data,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        if type == "album":
            data = []
            items = response_json["albums"]["items"]
            for item in items:
                data.append({
                    "record_artist": ", ".join([a["name"] for a in item["artists"]]),
                    "record_name": item["name"],
                    "spotify_uri": item["uri"],
                    "record_thumbnail": item["images"][0]["url"],
                })
            return data
        elif type == "playlist":
            data = []
            items = response_json["playlists"]["items"]
            for item in items:
                data.append({
                    "record_name": item["name"],
                    "uri": item["uri"],
                    "record_thumbnail": item["images"][0]["url"],
                })
            return data
        else:
            data = []
            items = response_json["tracks"]["items"]
            for item in items:
                data.append({
                    "record_artist": ", ".join([a["name"] for a in item["artists"]]),
                    "record_name": item["name"],
                    "spotify_uri": item["uri"],
                    "record_thumbnail": item["album"]["images"][0]["url"],
                })
            return data

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
            "spotify_duration_ms": response_json["duration_ms"],
            "spotify_name": response_json["name"][:32],
        }

    def get_album_info(self, spotify_uri):
        spotify_id = spotify_uri[14:]
        response = requests.get(
            f"https://api.spotify.com/v1/albums/{spotify_id}/tracks",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        items = response_json["items"]
        data = []
        for item in items:
            data.append({
                "spotify_uri": item["uri"],
                "spotify_duration_ms": item["duration_ms"],
                "spotify_name": item["name"],
            })
        return data

    def get_playlist_info(self, spotify_uri):
        spotify_id = spotify_uri[17:]
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{spotify_id}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        items = response_json["tracks"]["items"]
        data = []
        for item in items:
            data.append({
                "spotify_uri": track["track"]["uri"],
                "spotify_duration_ms": track["track"]["duration_ms"],
                "spotify_name": track["track"]["name"],
            })
        return data

    def get_me(self):
        response = requests.get(
            'https://api.spotify.com/v1/me/',
            headers={
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json',
            },
        )
        return response.json()

    async def get_user_info_async(self):
        response = await requests_async.get(
            "https://api.spotify.com/v1/me",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()
        response.raise_for_status()

    async def get_currently_playing_async(self):
        response = await requests_async.get(
            "https://api.spotify.com/v1/me/player/currently-playing",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()
        return {
            "spotify_ms": response_json["progress_ms"],
            "spotify_uri": response_json["item"]["uri"],
            "spotify_is_playing": response_json["is_playing"],
        }
