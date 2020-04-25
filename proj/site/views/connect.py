from cryptography.fernet import Fernet
import requests

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from proj import secrets
from proj.core.views import BaseView
from proj.core.resources import Spotify


@method_decorator(login_required, name="dispatch")
class ConnectView(BaseView):
    def get(self, request, **kwargs):
        """
        Connect the user's account to Spotify.
        """
        code = request.GET.get("code", None)

        current_site = get_current_site(request)
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": f"{secrets.SPOTIFY_HTTP}://{current_site}/connect",
                "client_id": secrets.SPOTIFY_CLIENT_ID,
                "client_secret": secrets.SPOITFY_CLIENT_SECRET,
            },
        )
        response_json = response.json()

        spotify = Spotify(request.user)
        spotify.store_access_token(response_json["access_token"])
        spotify.store_refresh_token(response_json["refresh_token"])

        if not request.user.profile.default_display_name:
            response_json = spotify.get_me()
            my_name = response_json['display_name']
            request.user.profile.default_display_name = my_name
            request.user.profile.save()

        if request.user.profile.activated_stream_redirect:
            stream_uuid_str = str(request.user.profile.activated_stream_redirect)
            request.user.profile.activated_stream_redirect = None
            request.user.profile.save()
            return self.redirect_response(f"/stream/{stream_uuid_str}")
        else:
            return self.redirect_response("/")
