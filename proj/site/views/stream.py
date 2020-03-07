from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


class StreamView(BaseView):
    def get(self, request, stream, **kwargs):
        Stream = apps.get_model('music', 'Stream')
        Ticket = apps.get_model('music', 'Ticket')

        if not request.user.is_authenticated:
            return self.redirect_response('/')

        ticket = (
            Ticket.objects
            .select_related('stream')
            .get(holder=request.user, stream__uuid=stream)
        )
        stream = ticket.stream

        is_host = request.user == stream.owner

        return self.template_response(
            request,
            'stream.html',
            {
                'stream': stream,
                'ticket': ticket,
                'is_host': is_host,
            }
        )
