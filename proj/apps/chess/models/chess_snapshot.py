
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.chess.models.managers import ChessSnapshotManager
from proj.apps.chess.models.querysets import ChessSnapshotQuerySet


class ChessSnapshot(models.Model):

    objects = ChessSnapshotManager.from_queryset(ChessSnapshotQuerySet)()

    # - - - - - - - -
    # config actions
    # - - - - - - - -

    ACTION_JOIN_MATCH = 'join_match'

    ACTION_CLOSE_MATCH = 'close_match'
    ACTION_RESIGN = 'resign'

    ACTION_TAKE_MOVE = 'take_move'
    ACTION_UNDO_MOVE = 'undo_move'
    ACTION_SUGGEST_MOVE = 'suggest_move'

    ACTION_ASK_UNDO_REQUEST = 'ask_undo_request'
    ACTION_APPROVE_UNDO_REQUEST = 'approve_undo_request'
    ACTION_REJECT_UNDO_REQUEST = 'reject_undo_request'

    ACTION_CHOICES = (
        ACTION_JOIN_MATCH,
        ACTION_CLOSE_MATCH,
        ACTION_RESIGN,
        ACTION_DECLINE_REMATCH,
        ACTION_TAKE_MOVE,
        ACTION_SUGGEST_MOVE,
        ACTION_ASK_UNDO_REQUEST,
        ACTION_APPROVE_UNDO_REQUEST,
        ACTION_REJECT_UNDO_REQUEST,
        ACTION_UNDO_MOVE,
    )

    # - - - - - -
    # properties
    # - - - - - -

    created_at = models.DateTimeField(
        default=datetime.datetime.now
    )

    action = models.CharField()
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='actors',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    board = models.CharField(
        max_length=92,
    )

    game = models.ForeignKey(
        'chess.ChessGame',
        related_name='snapshots',
        on_delete=models.DO_NOTHING,
    )

    step = models.IntegerField()

    # - - - - -
    # methods
    # - - - - -

    def create(self, *args, **kwargs):
        '''
        Override default create method to set defaults for `board` and `step`.
        '''
        from .models import ChessGame

        game = kwargs.get('game', None)
        if game:
            raise ValueError('ChessSnapshot must have an associated game.')

        if not kwargs.get('board', None):
            kwargs['board'] = game.board

        if not kwargs.get('step', None):
            kwargs['step'] = game.steps

        return super.create(*args, **kwargs)
