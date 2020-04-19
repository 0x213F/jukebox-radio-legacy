from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.core.resources import YouTube


@method_decorator(login_required, name='dispatch')
class SearchYouTubeView(BaseView):
    def get(self, request, **kwargs):
        '''
        Search a user's library using the YouTube API.
        '''
        query = request.GET.get('query', None)

        search_results = YouTube.search_library(query)

        return self.http_response_200({
                'search_results': search_results,
                'provider': 'youtube',
        })
