import uuid as _uuid

from django.conf import settings
from django.db import models

from proj.apps.music.models.managers import TicketManager
from proj.apps.music.models.querysets import TicketQuerySet
from proj.core.models import BaseModel


class Ticket(BaseModel):

    # - - - - - - -
    # config model |
    # - - - - - - -

    class Meta:
        abstract = False

    objects = TicketManager.from_queryset(TicketQuerySet)()

    def __str__(self):
        return f"({self.holder}) @ {self.stream}"

    # - - - -
    # fields |
    # - - - -

    uuid = models.UUIDField(default=_uuid.uuid4, editable=False)

    stream = models.ForeignKey(
        "music.Stream", related_name="tickets", on_delete=models.DO_NOTHING,
    )

    email = models.CharField(max_length=64, editable=False)
    holder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="tickets",
        on_delete=models.DO_NOTHING,
    )

    name = models.CharField(max_length=32, editable=False)
    is_active = models.BooleanField(default=False)

    is_hidden_when_idle = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
