
import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class ConnectView(BaseView):

    def get(self, request, **kwargs):
        '''
        Connect the user's account to Spotify.
        '''
        source = request.GET.get('source', None)
        code = request.GET.get('code', None)

        current_site = get_current_site(request)
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': f'http://{current_site}/connect?source={source}',
                'client_id': '890e3c32aaac4e0fa3dd5cfc22835f11',
                'client_secret': 'ce1072297bb0469e9adf1820c38616fa',
            }
        )
        response_json = response.json()
        request.user.profile.spotify_access_token = response_json['access_token']
        request.user.profile.spotify_refresh_token = response_json['refresh_token']
        request.user.profile.spotify_scope = response_json['scope']
        request.user.profile.save()

        if source == 'admin':
            messages.add_message(request, messages.SUCCESS, 'Spotify was successfully authorized')
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/')
