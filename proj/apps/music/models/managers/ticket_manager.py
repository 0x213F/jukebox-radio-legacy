from proj.core.models.managers import BaseManager


class TicketManager(BaseManager):
    '''
    Django Manager used to manage Comment objects.
    '''

    def serialize(self, ticket):
        if not ticket:
            return None
        print(ticket.name)
        return {
            'holder_name': ticket.name,
            'holder_uuid': str(ticket.holder_uuid),
            'holder_is_subscribed': ticket.is_subscribed,
            'email': ticket.email,
        }

    def promote_to_host(self, email, stream):
        ticket, _ = Ticket.objects.get_or_create(
            stream=stream,
            email=email,
            defaults={
                'name': generate_username(1)[0],
                'stream': stream,
                'status': Ticket.STATUS_ADDED_AS_HOST,
                'updated_at': datetime.now(),
            }
        )
        ticket.is_administrator = True
        ticket.save()

    def demote_from_host(self, email):
        Ticket.objects.filter(stream=stream, email=email).update(is_administrator=False)
