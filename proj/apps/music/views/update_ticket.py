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

        stream_uuid = request.POST.get('stream_uuid', None)
        holder_name = request.POST.get('display_name', None)

        email = request.POST.get('email', None)
        is_administrator = request.POST.get('is_administrator', None)
        is_administrator = True if is_administrator == 'true' else False

        ticket = Ticket.objects.select_related('stream').get(
            holder=request.user,
            stream__uuid=stream_uuid,
        )

        if email:
            assert ticket.stream.owner == request.user
            assert email != request.user.email

            name = (
                request.user.profile.default_display_name
                or generate_username(1)[0]
            )
            now = datetime.now()

            upgrade_ticket, _ = Ticket.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'stream': ticket.stream,
                    'status': Ticket.STATUS_ADDED_AS_HOST,
                    'updated_at': now,
                }
            )
            if is_administrator and upgrade_ticket.is_administrator:
                raise Exception('Already an admin')
            upgrade_ticket.is_administrator = is_administrator
            upgrade_ticket.save()
            return self.http_response({})

        if holder_name:
            ticket.name = holder_name
            ticket.save()

        if ticket.stream.owner_id == request.user.id:
            ticket.stream.owner_name = holder_name
            ticket.stream.save()

        return self.http_response({})
