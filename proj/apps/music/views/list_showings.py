
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.apps.music.models import Comment
from proj.apps.music.models import Showing
from proj.apps.users.models import Profile


@method_decorator(login_required, name='dispatch')
class ListShowingsView(BaseView):

    def get(self, request, **kwargs):
        '''
        List all of the showing objects that a user can access.
        '''
        showings = Showing.objects.list_showings(request.user)
        response = {
            'showings': [Showing.objects.serialize(s) for s in showings],
            'user': Profile.objects.serialize_user(request.user),
        }
        return self.http_response(response)
