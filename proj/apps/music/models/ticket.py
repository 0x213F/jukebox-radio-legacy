
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.music.models.managers import TicketManager
from proj.apps.music.models.querysets import TicketQuerySet

from proj.core.models import BaseModel


class Ticket(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False

    objects = TicketManager.from_queryset(TicketQuerySet)()

    def __str__(self):
        return f'User ({self.holder_id}) @ {self.showing}'

    # - - - -
    # fields
    # - - - -

    holder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tickets',
        on_delete=models.DO_NOTHING,
    )
    is_admin = models.BooleanField(default=False)
    showing = models.ForeignKey(
        'music.Showing',
        related_name='tickets',
        on_delete=models.DO_NOTHING,
    )
    timestamp_join = models.DateTimeField(auto_now_add=True)
    timestamp_last_active = models.DateTimeField(auto_now_add=True)
    display_name = models.CharField(max_length=32, editable=False)
