
from proj.core.models.managers import BaseManager


class TrackManager(BaseManager):
    '''
    Django Manager used to manage Track objects.
    '''
    pass

    # async def play_track_async(self, action, spotify_access_token):
    #     response = requests.put(
    #         f'https://api.spotify.com/v1/me/player/{action}',
    #         headers={
    #             'Authorization': f'Bearer {spotify_access_token}',
    #             'Content-Type': 'application/json',
    #         },
    #     )
    #
    # async def pause_track_async(self, action, spotify_access_token):
    #     response = requests.put(
    #         f'https://api.spotify.com/v1/me/player/{action}',
    #         headers={
    #             'Authorization': f'Bearer {spotify_access_token}',
    #             'Content-Type': 'application/json',
    #         },
    #     )
    #
    #
    # async def next_track_async(self, action, spotify_access_token):
    #     response = requests.post(
    #         f'https://api.spotify.com/v1/me/player/{action}',
    #         headers={
    #             'Authorization': f'Bearer {spotify_access_token}',
    #             'Content-Type': 'application/json',
    #         },
    #     )
    #
    # async def prev_track_async(self, action, spotify_access_token):
    #     response = requests.put(
    #         f'https://api.spotify.com/v1/me/player/{action}',
    #         headers={
    #             'Authorization': f'Bearer {spotify_access_token}',
    #             'Content-Type': 'application/json',
    #         },
    #     )
