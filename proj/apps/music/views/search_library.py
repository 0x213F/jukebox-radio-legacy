from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.core.resources import Spotify


@method_decorator(login_required, name='dispatch')
class SearchLibraryView(BaseView):

    def get(self, request, **kwargs):
        '''
        Search the user's library.
        '''
        query = request.GET.get('query', None)
        type = request.GET.get('type', None)

        spotify = Spotify(request.user)
        search_results = spotify.search_library(query, type)

        return self.http_response({
            'search_results': search_results,
            'type': type,
        })
