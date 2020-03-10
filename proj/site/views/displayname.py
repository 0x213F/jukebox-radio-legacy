from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


class DisplayNameView(BaseView):
    def get(self, request, stream, **kwargs):
        if not request.user.is_authenticated:
            return self.redirect_response('/')
        Ticket = apps.get_model('music', 'Ticket')

        ticket = (
            Ticket.objects
            .select_related('stream')
            .get(holder=request.user, stream__uuid=stream)
        )
        stream = ticket.stream

        return self.template_response(request, 'displayname.html', {
            'stream': stream,
            'ticket': ticket,
            'should_display_chat_button': False,
            'should_display_volume_button': False,
        })
