from urllib.parse import urlencode

from django.contrib.sites.shortcuts import get_current_site


SOURCE_USER = "user"
SOURCE_ADMIN = "admin"

SOURCE_CHOICES = (
    SOURCE_USER,
    SOURCE_ADMIN,
)


class Spotify:
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
