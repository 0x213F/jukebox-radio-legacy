
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.chess.models.managers import ChessSnapshotManager
from proj.apps.chess.models.querysets import ChessSnapshotQuerySet

class ChessSnapshot(models.Model):

    # - - - - - -
    # properties
    # - - - - - -

    objects = ChessSnapshotManager.from_queryset(ChessSnapshotQuerySet)()

    created_at = models.DateTimeField(
        default=datetime.datetime.now
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='actors',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    move = models.BooleanField()

    step = models.IntegerField()

    is_executed = models.BooleanField()

    # - - - - -
    # methods
    # - - - - -
    def create(self, *args, **kwargs):
        '''
        Override default create method.
        '''
        from .models import ChessGame

        code = kwargs.pop('code', False)
        if code:
            raise ValueError('ChessGame.code must be randomly generated.')

        # randomly generate a code
        while True:
            code = self.generate_code()
            if ChessGame.objects.active().filter(code=code).exists():
                continue
            break

        kwargs['code'] = code
        return super.create(*args, **kwargs)
