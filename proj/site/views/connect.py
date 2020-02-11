from cryptography.fernet import Fernet
import requests

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from proj import secrets
from proj.core.views import BaseView


@method_decorator(login_required, name="dispatch")
class ConnectView(BaseView):
    def get(self, request, **kwargs):
        """
        Connect the user's account to Spotify.
        """
        source = request.GET.get("source", None)
        code = request.GET.get("code", None)

        current_site = get_current_site(request)
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": f"http://{current_site}/connect?source={source}",
                "client_id": secrets.SPOTIFY_CLIENT_ID,
                "client_secret": secrets.SPOTIFY_CLIENT_SECRET,
            },
        )
        response_json = response.json()

        cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)
        cipher_spotify_access_token = cipher_suite.encrypt(
            response_json["access_token"].encode("utf-8")
        )
        cipher_spotify_refresh_token = cipher_suite.encrypt(
            response_json["refresh_token"].encode("utf-8")
        )

        request.user.profile.spotify_access_token = cipher_spotify_access_token.decode(
            "utf-8"
        )
        request.user.profile.spotify_refresh_token = cipher_spotify_refresh_token.decode(
            "utf-8"
        )
        request.user.profile.spotify_scope = response_json["scope"]
        request.user.profile.save()

        if source == "admin":
            messages.add_message(
                request, messages.SUCCESS, "Spotify was successfully authorized"
            )
            return HttpResponseRedirect("/admin")
        else:
            print('ok here!!!')
            return HttpResponseRedirect("/")
