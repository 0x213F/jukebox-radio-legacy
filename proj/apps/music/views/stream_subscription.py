
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView
from proj.apps.music.models import Comment
from proj.apps.music.models import Ticket
from proj.apps.music.models import Stream
from proj.apps.users.models import Profile


SUBSCRIBED = 'subscribed'
UNSUBSCRIBED = 'unsubscribed'


@method_decorator(login_required, name='dispatch')
class StreamSubscriptionView(BaseView):

    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Ticket = apps.get_model('music.Ticket')

        stream_uuid = request.POST.get('stream_uuid', None)
        status = request.POST.get('status', None)

        ticket = Ticket.objects.get(holder=request.user, stream__uuid=stream_uuid)

        if status == SUBSCRIBED:
            ticket.is_subscribed = True
        else:  # status == UNSUBSCRIBED:
            ticket.is_subscribed = False
        ticket.save()
        return self.http_response({})
