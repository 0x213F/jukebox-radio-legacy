
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from .managers import ChessManager
from .querysets import ChessQuerySet

class Chess(models.Model):

    objects = ChessManager.from_queryset(ChessQuerySet)()

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    board = models.CharField(max_length=92)

    black = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blacks',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    white = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='whites',
        on_delete=models.DO_NOTHING,
        null=True,
    )
