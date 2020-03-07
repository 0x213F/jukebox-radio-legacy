from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class UpdateTicketView(BaseView):

    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Ticket = apps.get_model('music.Ticket')

        holder_uuid = request.POST.get('holder_uuid', None)
        email = request.POST.get('email', None)
        stream_uuid = request.POST.get('stream_uuid', None)
        holder_name = request.POST.get('display_name', None)

        is_administrator = request.POST.get('is_administrator', None)
        is_administrator = True if is_administrator == 'true' else False

        ticket = Ticket.objects.get(
            holder=request.user,
            stream__uuid=stream_uuid,
        )

        if email:
            assert ticket.stream.owner == request.user
            ticket = Ticket.objects.get(
                holder__email=email,
                stream__uuid=stream_uuid,
            )
            if is_administrator and ticket.is_administrator:
                raise Excpection('already an admin')
            ticket.is_administrator = is_administrator
        elif holder_uuid:
            assert ticket.stream.owner == request.user
            ticket = Ticket.objects.get(
                stream__uuid=stream_uuid,
                holder_uuid=holder_uuid,
            )
            ticket.is_administrator = is_administrator
        else:
            if holder_name:
                ticket.holder_name = holder_name
            if is_administrator:
                ticket.is_administrator = is_administrator

        ticket.save()

        return self.http_response({})
