from django.apps import apps
from django.db.models import Exists, OuterRef

from proj.core.models.querysets import BaseQuerySet


class StreamQuerySet(BaseQuerySet):
    """
    Django QuerySet used to query Stream objects.
    """

    def list_broadcasting_streams(self, user):
        """
        QuerySet of stream objects where the user has host access.
        """
        Ticket = apps.get_model("music", "Ticket")
        return self.filter(
            Exists(
                Ticket.objects.filter(
                    stream_id=OuterRef("id"),
                    email=user.email,
                    is_administrator=True,
                    is_hidden_when_idle=False,
                )
            )
        )

    def list_tune_in_streams(self, user):
        """
        QuerySet of stream objects which are public and the user does not have
        host access.
        """
        Stream = apps.get_model("music", "Stream")
        Ticket = apps.get_model("music", "Ticket")
        return (
            self.filter(status=Stream.STATUS_ACTIVATED)
            .exclude(
                Exists(
                    Ticket.objects.filter(
                        stream_id=OuterRef("id"),
                        email=user.email,
                        is_administrator=True,
                    )
                )
            )
            .exclude(is_private=True)
        )
