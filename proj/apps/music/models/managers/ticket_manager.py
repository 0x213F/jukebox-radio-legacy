from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from random_username.generate import generate_username

from django.contrib.auth.models import User

from proj.core.models.managers import BaseManager


channel_layer = get_channel_layer()


class TicketManager(BaseManager):
    '''
    Django Manager used to manage Comment objects.
    '''

    def serialize(self, ticket):
        if not ticket:
            return None
        return {
            'holder_name': ticket.name,
            'holder_uuid': str(ticket.uuid),
            'email': ticket.email,
        }

    def promote_to_host(self, email, stream):
        Ticket = self.model

        ticket, _ = Ticket.objects.get_or_create(
            stream=stream,
            email=email,
            defaults={
                'name': generate_username(1)[0],
                'stream': stream,
                'updated_at': datetime.now(),
            },
        )
        ticket.is_administrator = True
        ticket.save()

        user = User.objects.get(email__iexact=email)
        async_to_sync(channel_layer.group_send)(
            f'user-{user.id}', {'type': 'promote_to_host',},
        )

    def demote_from_host(self, email, stream):
        Ticket = self.model

        Ticket.objects.filter(stream=stream, email=email).update(is_administrator=False)

        user = User.objects.get(email__iexact=email)
        async_to_sync(channel_layer.group_send)(
            f'user-{user.id}', {'type': 'demote_from_host',},
        )
