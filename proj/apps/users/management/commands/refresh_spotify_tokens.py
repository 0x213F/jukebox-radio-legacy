
import requests

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refreshes Spotify API tokens'

    def handle(self, *args, **options):
        Profile = apps.get_model('users.Profile')

        profiles_to_refresh = (
            Profile
            .objects
            .filter(spotify_access_token__isnull=False)
        )
        for profile in profiles_to_refresh:
            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': profile.spotify_refresh_token,
                    'client_id': '890e3c32aaac4e0fa3dd5cfc22835f11',
                    'client_secret': 'ce1072297bb0469e9adf1820c38616fa',
                }
            )
            response_json = response.json()
            profile.spotify_access_token = response_json['access_token']
            profile.spotify_scope = response_json['scope']
            profile.save()
