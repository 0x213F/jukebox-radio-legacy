import uuid
from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


class StreamView(BaseView):
    def get(self, request, stream, **kwargs):
        Stream = apps.get_model('music', 'Stream')
        Ticket = apps.get_model('music', 'Ticket')

        if not request.user.is_authenticated:
            return self.redirect_response(f'/linkspotify?stream_uuid={stream}')

        try:
            ticket = (
                Ticket.objects
                .get(holder=request.user, stream__uuid=stream)
            )
            stream = ticket.stream
        except Ticket.DoesNotExist:
            stream = Stream.objects.get(uuid=stream)
            ticket = Ticket.objects.create(
                holder=request.user,
                stream=stream,
                timestamp_last_active=datetime.utcnow(),
                holder_name=request.user.profile.default_display_name or generate_username(1)[0],
                holder_uuid=uuid.uuid4(),
            )

        is_host = request.user == stream.owner

        return self.template_response(
            request,
            'stream.html',
            {
                'stream': stream,
                'ticket': ticket,
                'is_host': is_host,
                'should_display_queue_button': True,
            }
        )
