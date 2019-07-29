
import chess

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from proj.apps.music.models import Comment
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
        last_active_comment = (
            Comment.objects
            .filter(
                commenter=request.user,
                showing__in=showings,
                status__in=[Comment.STATUS_JOINED, Comment.STATUS_LEFT]
            ).order_by('-created_at').first()
        )
        if last_active_comment and last_active_comment.status == Comment.STATUS_JOINED:
            active_showing = last_active_comment.showing
            response['active_showing'] = {
                'id': active_showing.id,
                'status': active_showing.status,
                'showtime': active_showing.scheduled_showtime,
                'actual_showtime': active_showing.actual_showtime,
                'album': {
                    'art': active_showing.album.art,
                    'name': active_showing.album.name,
                    'artist': {
                        'name': active_showing.album.artist.name,
                    }
                }
            }

        request.user.refresh_from_db()

        response['me'] = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'display_name': request.user.profile.display_name,
        }

        return self.http_response(response)
