
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.chess.models.managers import ChessGameManager
from proj.apps.chess.models.querysets import ChessGameQuerySet


class ChessGame(models.Model):

    objects = ChessGameManager.from_queryset(ChessGameQuerySet)()

    # - - - - - - - - -
    # config join code
    # - - - - - - - - -

    JOIN_CODE_LENGTH = 4

    # - - - - - - - -
    # config players
    # - - - - - - - -

    PLAYER_BLACK = 'black'
    PLAYER_WHITE = 'white'

    PLAYER_CHOICES = (
        PLAYER_BLACK,
        PLAYER_WHITE
    )

    # - - - - - - - -
    # config status
    # - - - - - - - -

    STATUS_PENDING_WAITING = 'pending_game_start'
    STATUS_PENDING_EMPTY = 'pending_opponent'
    STATUS_WARNING_GAME_CANCELLATION = 'warning_game_cancellation'
    STATUS_COMPLETE = 'complete'

    STATUS_MY_TURN = 'my_turn'
    STATUS_THEIR_TURN = 'their_turn'

    STATUS_CHOICES = (
        (STATUS_PENDING_WAITING, STATUS_PENDING_WAITING),
        (STATUS_PENDING_EMPTY, STATUS_PENDING_EMPTY),
        (STATUS_WARNING_GAME_CANCELLATION, STATUS_WARNING_GAME_CANCELLATION),
        (STATUS_COMPLETE, STATUS_COMPLETE),
        (STATUS_MY_TURN, STATUS_MY_TURN),
        (STATUS_THEIR_TURN, STATUS_THEIR_TURN)
    )

    # - - - - - - - - -
    # config defaults
    # - - - - - - - - -

    DEFAULT_GAME_CLOCK_IN_SECONDS = 3000  # 5 minutes
    DEFAULT_MOVE_REBOUND_IN_SECONDS = 5

    # - - - - - - - - - - - -
    # identifier properties
    # - - - - - - - - - - - -

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    join_code = models.CharField(
        editable=False,
        max_length=JOIN_CODE_LENGTH,
    )

    # - - - - - - - - -
    # time properties
    # - - - - - - - - -

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

    # - - - - - - - - -
    # configuration properties
    # - - - - - - - - -

    is_private = models.BooleanField()
    game_clock = models.FloatField(
        default=DEFAULT_GAME_CLOCK_IN_SECONDS,
    )
    move_rebound = models.FloatField(
        default=DEFAULT_MOVE_REBOUND_IN_SECONDS,
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
        default=DEFAULT_GAME_CLOCK_IN_SECONDS,
    )

    black_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=32,
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
        default=DEFAULT_GAME_CLOCK_IN_SECONDS,
    )

    white_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=32,
    )

    # - - - -
    # state
    # - - - -

    steps = models.IntegerField(
        default=0,
    )

    board = models.CharField(
        max_length=92,
    )

    # - - - - -
    # methods
    # - - - - -

    def create(self, *args, **kwargs):
        '''
        Override default create method to allow random generated join code.
        '''
        from .models import ChessGame

        black_user = kwargs.get('black_user', None)
        white_user = kwargs.get('black_user', None)

        kwargs = self._set_default_attribute('black_status')
        kwargs = self._set_default_attribute('white_status')
        self._assert_attribute_not_in_kwargs('code')
        white_status = kwargs.pop('white_status', None)

        kwargs['black_status'] = self.STATUS_PENDING_EMPTY
        kwargs['white_status'] = self.STATUS_PENDING_EMPTY
        if not black_user and not white_user:
            raise ValueError('ChessGame must have at least one player.')
        if black_user:
            kwargs['black_user'] = self.STATUS_PENDING_WAITING
        if white_user:
            kwargs['white_user'] = self.STATUS_PENDING_WAITING

        # randomly generate a valid code
        while True:
            code = self.generate_code()
            if ChessGame.objects.active().filter(code=code).exists():
                continue
            break

        kwargs['code'] = code
        return super.create(*args, **kwargs)

    def get_player(self, user):
        '''
        todo: docstring
        '''
        if self.black == user:
            return 'black'
        elif self.white == user:
            return 'white'
        else:
            raise Exception('User not in game.')

    def get_opponent(self, user):
        if self.black == user:
            return 'white'
        elif self.white == user:
            return 'black'
        else:
            raise Exception('User not in game.')
