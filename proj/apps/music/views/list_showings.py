
import chess

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from proj.apps.music.models import Showing

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class ListShowingsView(BaseView):
    '''
    TODO docstring
    '''

    def get(self, request, **kwargs):
        '''
        TODO docstring
        '''
        showings = (
            Showing.objects.select_related('album', 'album__artist')
            .filter(status=Showing.STATUS_SCHEDULED)
        )
        response = {'scheduled_showings': []}
        for showing in showings:
            response['scheduled_showings'].append({
                'id': showing.id,
                'status': showing.status,
                'showtime': showing.scheduled_showtime,
                'actual_showtime': showing.actual_showtime,
                'album': {
                    'art': showing.album.art,
                    'name': showing.album.name,
                    'artist': {
                        'name': showing.album.artist.name,
                    }
                }
            })
        return self.http_response(response)
