from proj.core.models.querysets import BaseQuerySet

from django.apps import apps
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models import IntegerField


class StreamQuerySet(BaseQuerySet):
    """
    Django QuerySet used to query Stream objects.
    """

    def list_streams(self, user):
        """
        QuerySet of stream objects that a user can access.
        """
        Stream = self.model
        return self.filter(status__in=(Stream.STATUS_ACTIVATED,))


    def list_broadcasting_streams(self, user):
        """
        QuerySet of stream objects that a user can access.
        """
        Ticket = apps.get_model('music', 'Ticket')
        return self.filter(
            Exists(
                Ticket.objects.filter(
                    stream_id=OuterRef('id'),
                    holder=user,
                    is_administrator=True,
                )
            )
        )
