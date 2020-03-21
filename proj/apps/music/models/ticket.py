import uuid as _uuid

from django.conf import settings
from django.db import models

from proj.apps.music.models.managers import TicketManager
from proj.apps.music.models.querysets import TicketQuerySet

from proj.core.models import BaseModel


class Ticket(BaseModel):

    STATUS_CREATED_STREAM = 'created_stream'
    STATUS_ADDED_AS_HOST = 'added_as_host'

    # - - - - - - -
    # config model |
    # - - - - - - -

    class Meta:
        abstract = False

    objects = TicketManager.from_queryset(TicketQuerySet)()

    def __str__(self):
        return f'User ({self.holder_id}) @ {self.stream}'

    # - - - -
    # fields |
    # - - - -

    stream = models.ForeignKey(
        'music.Stream', related_name='tickets', on_delete=models.DO_NOTHING,
    )

    holder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='tickets',
        on_delete=models.DO_NOTHING,
    )
    email = models.CharField(max_length=64, editable=False)
    name = models.CharField(max_length=32, editable=False)
    uuid = models.UUIDField(default=_uuid.uuid4, editable=False)

    is_administrator = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    is_listed = models.BooleanField(default=False)

    status = models.CharField(max_length=32, editable=False)
    updated_at = models.DateTimeField(null=True, blank=False)

    # to be removed later
    holder_uuid = models.UUIDField(default=_uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
