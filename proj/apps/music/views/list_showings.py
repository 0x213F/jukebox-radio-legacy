
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.apps.music.models import Comment
from proj.apps.music.models import Ticket
from proj.apps.music.models import Showing
from proj.apps.users.models import Profile


@method_decorator(login_required, name='dispatch')
class ListShowingsView(BaseView):

    def get(self, request, **kwargs):
        '''
        List all of the showing objects that a user can access.
        '''
        showings = Showing.objects.list_showings(request.user)
        print(showings[0].__dict__)

        active_ticket = None
        active_showing_uuid = request.user.profile.active_showing_uuid
        print(active_showing_uuid)
        if active_showing_uuid:
            active_ticket = Ticket.objects.get(
                holder=request.user,
                showing__uuid=active_showing_uuid,
            )
        response = {
            'showings': [Showing.objects.serialize(s) for s in showings],
            'user': (
                Profile.objects
                .serialize_user(request.user, active_ticket=active_ticket)
            ),
        }
        return self.http_response(response)
