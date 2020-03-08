from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class StreamSubscriptionView(BaseView):

    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Ticket = apps.get_model('music.Ticket')

        stream_uuid = request.POST.get('stream_uuid', None)
        status = request.POST.get('status', None)

        ticket = (
            Ticket
            .objects
            .get(holder=request.user, stream__uuid=stream_uuid)
        )

        if status == SUBSCRIBED:
            ticket.is_subscribed = True
        elif status == UNSUBSCRIBED:
            ticket.is_subscribed = False
        else:
            raise ValueError(f'Invalid status: {status}')

        ticket.save()

        return self.http_response({})
