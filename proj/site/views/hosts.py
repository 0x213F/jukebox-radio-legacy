import uuid

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


class HostsView(BaseView):
    def get(self, request, stream, **kwargs):
        Ticket = apps.get_model('music', 'Ticket')

        if not request.user.is_authenticated:
            return self.redirect_response('/')

        if not request.user.is_authenticated:
            return self.redirect_response('/')

        ticket = (
            Ticket.objects
            .select_related('stream')
            .get(
                holder=request.user,
                stream__uuid=stream,
                stream__owner=request.user,
            )
        )
        stream = ticket.stream
        stream.tags = ''.join(stream.tags.split(", "))

        return self.template_response(request, 'manage.html', {'stream': stream, 'ticket': ticket})
