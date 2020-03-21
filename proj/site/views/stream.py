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

        unique_custom_id = stream
        stream = Stream.objects.get(unique_custom_id=unique_custom_id)

        if stream.is_private:
            try:
                ticket = Ticket.objects.get(
                    stream=stream,
                    email=request.user.email,
                    is_administrator=True,
                )
            except Ticket.DoesNotExist:
                raise ValueError('User does not have access to private stream')
        else:
            ticket, _ = (
                Ticket.objects.get_or_create(
                    stream=stream,
                    email=request.user.email,
                    defaults={
                        'holder': request.user,
                        'name': request.user.profile.default_display_name or generate_username(1)[0],
                    }
                )
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
