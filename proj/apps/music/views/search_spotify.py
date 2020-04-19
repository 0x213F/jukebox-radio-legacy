from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.core.resources import Spotify


@method_decorator(login_required, name='dispatch')
class SearchSpotifyView(BaseView):
    def get(self, request, **kwargs):
        '''
        Search a user's library using the Spotify API.
        '''
        query = request.GET.get('query', None)
        type = request.GET.get('type', None)

        spotify = Spotify(request.user)
        search_results = spotify.search_library(query, type)

        return self.http_response_200({
            'search_results': search_results,
            'type': type,
            'provider': 'spotify',
        })
