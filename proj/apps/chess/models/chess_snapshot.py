
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.chess.models.managers import ChessSnapshotManager
from proj.apps.chess.models.querysets import ChessSnapshotQuerySet

from proj.core.models import BaseModel


class ChessSnapshot(BaseModel):
    '''
    Model which helps represent snapshots of a chess game to recreate a
    play-by-play historical reference of games.
    '''

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = ChessSnapshotManager.from_queryset(ChessSnapshotQuerySet)()

    # - - - - - - - -
    # config actions
    # - - - - - - - -

    ACTION_CREATE_MATCH = 'create_match'
    ACTION_JOIN_MATCH = 'join_match'
    ACTION_CLOSE_MATCH = 'close_match'
    ACTION_RESIGN_MATCH = 'resign_match'

    ACTION_TAKE_MOVE = 'take_move'
    ACTION_UNDO_MOVE = 'undo_move'
    ACTION_SUGGEST_MOVE = 'suggest_move'

    ACTION_CREATE_UNDO_REQUEST = 'create_undo_request'
    ACTION_APPROVE_UNDO_REQUEST = 'approve_undo_request'
    ACTION_REJECT_UNDO_REQUEST = 'reject_undo_request'

    # NOTE: These are methods accessible publically via the API. See the
    #       following files for more information:
    #
    # proj.core.models.managers.base_manager.py       # {API: method} mapping
    # proj.apps.chess.views.do.py                     # API endpoint
    # proj.apps.chess.managers.chess_game_manager.py  # methods
    ACTION_CHOICES = (
        (ACTION_CREATE_MATCH, ACTION_CREATE_MATCH),
        (ACTION_JOIN_MATCH, ACTION_JOIN_MATCH),
        (ACTION_CLOSE_MATCH, ACTION_CLOSE_MATCH),
        (ACTION_RESIGN_MATCH, ACTION_RESIGN_MATCH),
        (ACTION_TAKE_MOVE, ACTION_TAKE_MOVE),
        (ACTION_SUGGEST_MOVE, ACTION_SUGGEST_MOVE),
        (ACTION_CREATE_UNDO_REQUEST, ACTION_CREATE_UNDO_REQUEST),
        (ACTION_APPROVE_UNDO_REQUEST, ACTION_APPROVE_UNDO_REQUEST),
        (ACTION_REJECT_UNDO_REQUEST, ACTION_REJECT_UNDO_REQUEST),
        (ACTION_UNDO_MOVE, ACTION_UNDO_MOVE)
    )

    # - - - - - -
    # properties
    # - - - - - -

    created_at = models.DateTimeField(
        default=datetime.datetime.now
    )

    action = models.CharField(
        choices=ACTION_CHOICES,
        max_length=32,
    )

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
