import uuid

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


class ManageView(BaseView):
    def get(self, request, stream, **kwargs):
        Ticket = apps.get_model('music', 'Ticket')

        if not request.user.is_authenticated:
            return self.redirect_response('/')

        ticket = (
            Ticket.objects
            .select_related('stream')
            .get(
                email=request.user.email,
                stream__unique_custom_id=stream,
            )
        )
        stream = ticket.stream
        stream.tags = ''.join(stream.tags.split(", "))

        if stream.owner == request.user:
            return self.template_response(request, 'manage.html', {'stream': stream, 'ticket': ticket})
        else:
            return self.template_response(request, 'displayname.html', {'stream': stream, 'ticket': ticket})
