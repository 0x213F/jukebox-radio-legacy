
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from .managers import ChessManager
from .querysets import ChessQuerySet

class Chess(models.Model):

    # - - - - - - -
    # code config
    # - - - - - - -

    CODE_LENGTH = 4

    # - - - - - - - -
    # status config
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


    objects = ChessManager.from_queryset(ChessQuerySet)()

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

    code = models.CharField(
        editable=False,
        max_length=CODE_LENGTH,
    )

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

    # - - - - -
    # methods
    # - - - - -
    def create(self, *args, **kwargs):
        '''
        Override default create method.
        '''
        from .models import Chess

        code = kwargs.pop('code', False)
        if code:
            raise ValueError('Chess.code must be randomly generated.')

        # randomly generate a code
        while True:
            code = self.generate_code()
            if Chess.objects.active().filter(code=code).exists():
                continue
            break

        kwargs['code'] = code
        return super.create(*args, **kwargs)
