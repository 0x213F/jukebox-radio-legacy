from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.core.resources import Spotify
from proj.core.resources import YouTube


@method_decorator(login_required, name='dispatch')
class SearchView(BaseView):
    def get(self, request, **kwargs):
        '''
        Search a user's library
        '''
        query = request.GET.get('query', None)
        spotify_type = request.GET.get('spotify_type', None)
        provider = request.GET.get('provider', None)

        if provider == 'spotify':
            spotify = Spotify(request.user)
            search_results = spotify.search_library(query, spotify_type)

            return self.http_response_200({
                'search_results': search_results,
                'spotify_type': spotify_type,
                'provider': 'spotify',
            })

        if provider == 'youtube':
            search_results = YouTube.search_library(query)

            return self.http_response_200({
                    'search_results': search_results,
                    'provider': 'youtube',
            })

        if provider == 'soundcloud':
            raise NotImplimentedError()
