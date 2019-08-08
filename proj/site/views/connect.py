
import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class ConnectView(BaseView):

    def get(self, request, **kwargs):
        '''
        Connect the user's account to Spotify.
        '''
        source = request.GET.get('source', None)
        code = request.GET.get('code', None)

        response = requests.post(
            'https://accounts.spotify.com/api/token',
            # headers={
            #     'Authorization': 'Basic *<base64 encoded 890e3c32aaac4e0fa3dd5cfc22835f11:ce1072297bb0469e9adf1820c38616fa>*'
            # },
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'http://localhost:8000/connect?source=spotify',
                'client_id': '890e3c32aaac4e0fa3dd5cfc22835f11',
                'client_secret': 'ce1072297bb0469e9adf1820c38616fa',
            }
        )
        response_json = response.json()
        print(response_json)
        request.user.profile.spotify_access_token = response_json['access_token']
        request.user.profile.spotify_refresh_token = response_json['refresh_token']
        request.user.profile.spotify_scope = response_json['scope']
        return HttpResponseRedirect('/')
