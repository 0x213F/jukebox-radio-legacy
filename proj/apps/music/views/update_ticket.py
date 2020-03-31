from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime
from random_username.generate import generate_username

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class UpdateTicketView(BaseView):

    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Ticket = apps.get_model('music.Ticket')

        email = request.POST.get('email', None)
        holder_name = request.POST.get('display_name', None)
        is_administrator = request.POST.get('is_administrator', None)
        is_administrator = is_administrator == 'true'
        stream_uuid = request.POST.get('stream_uuid', None)

        ticket = Ticket.objects.select_related('stream').get(
            email=request.user.email,
            stream__uuid=stream_uuid,
        )
        stream = ticket.stream

        if email:
            if not stream.owner == request.user:
                raise ValueError(
                    'Authenticated user is not stream owner and is not '
                    'allowed to promote another user to host.'
                )
            if is_administrator:
                Ticket.objects.promote_to_host(email, stream)
            else:
                Ticket.objects.demote_from_host(email, stream)
        else:
            if holder_name:
                ticket.name = holder_name
                ticket.save()
            if ticket.stream.owner_id == request.user.id:
                ticket.stream.owner_name = holder_name
                ticket.stream.save()

        return self.http_response({})
