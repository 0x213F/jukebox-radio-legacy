from cryptography.fernet import Fernet
import requests
import sys

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from proj import secrets


class Command(BaseCommand):
    help = "Refreshes Spotify API tokens"

    def handle(self, *args, **options):
        Profile = apps.get_model("users.Profile")

        profiles_to_refresh = Profile.objects.filter(spotify_access_token__isnull=False)

        for profile in profiles_to_refresh:
            cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)
            spotify_refresh_token = cipher_suite.decrypt(
                profile.spotify_refresh_token.encode("utf-8")
            ).decode("utf-8")

            response = requests.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": spotify_refresh_token,
                    "client_id": secrets.SPOTIFY_CLIENT_ID,
                    "client_secret": secrets.SPOTIFY_CLIENT_SECRET,
                },
            )
            response_json = response.json()

            cipher_spotify_access_token = cipher_suite.encrypt(
                response_json["access_token"].encode("utf-8")
            )

            profile.spotify_access_token = cipher_spotify_access_token.decode("utf-8")
            profile.spotify_scope = response_json["scope"]
            profile.save()
