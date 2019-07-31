
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.apps.music.models import Comment
from proj.apps.music.models import Showing

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class ListShowingsView(BaseView):

    def get(self, request, **kwargs):
        '''
        List all of the showing objects that a user can access.
        '''
        response = {
            'showings': [],
            'active_showing': [],
            'user': {},
        }

        showings = Showing.objects.list_showings(request.user)
        for showing in showings:
            response['showings'].append(Showing.objects.serialize(showing))

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
            response['active_showing'] = Showing.objects.serialize(active_showing)

        request.user.refresh_from_db()
        response['user'] = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'display_name': request.user.profile.display_name,
        }

        return self.http_response(response)
