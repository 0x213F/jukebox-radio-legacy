from proj.core.models.querysets import BaseQuerySet


class TicketQuerySet(BaseQuerySet):
    """
    Django QuerySet used to query Ticket objects.
    """

    def administrators(self, stream):
        return self.filter(stream=stream, is_administrator=True)
