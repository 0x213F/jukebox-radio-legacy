
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.chess.models.managers import ChessGameManager
from proj.apps.chess.models.querysets import ChessGameQuerySet


class ChessGame(models.Model):

    # - - - - - - -
    # config join code
    # - - - - - - -

    JOIN_CODE_LENGTH = 4

    # - - - - - - - -
    # config status
    # - - - - - - - -

    STATUS_PENDING = 'pending'
    STATUS_WARNING = 'warning'
    STATUS_MY_TURN = 'my_turn'
    STATUS_THEIR_TURN = 'their_turn'
    STATUS_COMPLETE = 'complete'

    STATUS_CHOICES = (
        STATUS_PENDING,
        STATUS_WARNING,
        STATUS_MY_TURN,
        STATUS_THEIR_TURN,
        STATUS_COMPLETE,
    )

    # - - - - - - - - -
    # config defaults
    # - - - - - - - - -

    DEFAULT_USER_CLOCK_IN_SECONDS = 60 * 5

    DEFAULT_MOVE_BOUNCE_BACK_IN_SECONDS = 5

    # - - - - - - - - -
    # game properties
    # - - - - - - - - -

    objects = ChessGameManager.from_queryset(ChessGameQuerySet)()

    created_at = models.DateTimeField(
        default=datetime.datetime.now
    )

    started_at = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
    )

    finished_at = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
    )

    join_code = models.CharField(
        editable=False,
        max_length=JOIN_CODE_LENGTH,
    )

    board = models.CharField(
        max_length=92,
    )

    bounce_back = models.FloatField(
        default=DEFAULT_MOVE_BOUNCE_BACK_IN_SECONDS,
    )

    # - - - - - - - - -
    # black properties
    # - - - - - - - - -

    black_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blacks',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    black_time = models.FloatField(
        default=DEFAULT_USER_CLOCK_IN_SECONDS,
    )

    # - - - - - - - - -
    # white properties
    # - - - - - - - - -

    white_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='whites',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    white_time = models.FloatField(
        default=DEFAULT_USER_CLOCK_IN_SECONDS,
    )

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
