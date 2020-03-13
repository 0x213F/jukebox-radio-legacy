from cryptography.fernet import Fernet
import requests

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from proj.core.views import BaseView
from proj.core.resources import Spotify


@method_decorator(login_required, name='dispatch')
class ConnectView(BaseView):
    def get(self, request, **kwargs):
        '''
        Connect the user's account to Spotify.
        '''
        code = request.GET.get('code', None)

        current_site = get_current_site(request)
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': f'http://{current_site}/connect',
                'client_id': '133a25c7195344dbafd4f50d7450330f',
                'client_secret': '4029f523ad8a46cb86e29b9dd54cc257',
            },
        )
        response_json = response.json()

        spotify = Spotify(request.user)
        spotify.store_access_token(response_json['access_token'])
        spotify.store_refresh_token(response_json['refresh_token'])

        return self.redirect_response('/')
