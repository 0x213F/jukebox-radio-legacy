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
        '''
        Make a Ticket object JSON serializable.
        '''
        if not ticket:
            return None
        return {
            'name': ticket.name,
            'uuid': str(ticket.uuid),
            'email': ticket.email,
            'is_administrator': ticket.is_administrator,
            'status': ticket.status,
        }

    def promote_to_host(self, email, stream):
        '''
        Promote user to host. If the user doesn't exist, create a ticket to
        hold their seat via email. If the user is currently in the stream, ping
        them so their UI is updated with added host controls.
        '''
        Profile = apps.get_model('users', 'Profile')
        Ticket = self.model

        ticket, created = Ticket.objects.get_or_create(
            stream=stream,
            email=email,
            defaults={
                'name': generate_username(1)[0],
                'stream': stream,
                'status': Ticket.STATUS_ADDED_AS_HOST,
                'updated_at': datetime.now(),
                'is_administrator': True,
            },
        )

        if not created:
            ticket.is_administrator = True
            ticket.save()

        try:
            user = User.objects.get(email__iexact=email)
            async_to_sync(channel_layer.group_send)(
                f'user-{user.id}',
                {
                    'type': 'send_update',
                    'text': {
                        'updated': {
                            'users': [Profile.objects.serialize_user(
                                user, active_ticket=ticket
                            )],
                        }
                    }
                },
            )
        except User.DoesNotExist:
            pass

    def demote_from_host(self, email, stream):
        '''
        Demote user from host. If the user is currently in the stream, ping
        them so their UI is updated with removed host controls. If the user has
        not created an account yet, pass.
        '''
        Ticket = self.model

        ticket = Ticket.objects.select_related('holder').get(stream=stream, email=email)

        ticket.is_administrator = False
        ticket.save()

        try:
            user = ticket.holder
            async_to_sync(channel_layer.group_send)(
                f'user-{user.id}',
                {
                    'type': 'send_update',
                    'text': {
                        'updated': {
                            'users': [Profile.objects.serialize_user(
                                user, active_ticket=ticket
                            )],
                        }
                    }
                },
            )
        except User.DoesNotExist:
            pass
