import sys

import requests
from cryptography.fernet import Fernet
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from proj import secrets
from proj.core.resources import Spotify


class Command(BaseCommand):
    help = "Refreshes Spotify API tokens"

    def handle(self, *args, **options):
        Profile = apps.get_model("users.Profile")

        user_qs = User.objects.filter(profile__spotify_access_token__isnull=False,)

        for user in user_qs:
            try:
                spotify = Spotify(user)
                spotify_refresh_token = spotify.refresh_token

                response = requests.post(
                    "https://accounts.spotify.com/api/token",
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": spotify_refresh_token,
                        "client_id": secrets.SPOTIFY_CLIENT_ID,
                        "client_secret": secrets.SPOITFY_CLIENT_SECRET,
                    },
                )
                response_json = response.json()

                spotify.store_access_token(response_json["access_token"])

                user.profile.spotify_scope = response_json["scope"]
                user.profile.save()
            except Exception as e:
                user.profile.spotify_access_token = None
                user.profile.spotify_refresh_token = None
                user.profile.spotify_scope = None
                user.profile.save()
                pass
