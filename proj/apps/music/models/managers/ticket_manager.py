
from proj.core.models.managers import BaseManager


class TicketManager(BaseManager):
    '''
    Django Manager used to manage Comment objects.
    '''

    def serialize(self, ticket):
        if not ticket:
            return None
        return {
            'holder_name': ticket.holder_name,
            'holder_uuid': str(ticket.holder_uuid),
            'holder_is_subscribed': ticket.is_subscribed,
        }
