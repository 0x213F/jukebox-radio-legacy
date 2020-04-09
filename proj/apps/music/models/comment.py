from datetime import datetime

from django.conf import settings
from django.db import models

from proj.apps.music.models.managers import CommentManager
from proj.apps.music.models.querysets import CommentQuerySet

from proj.core.models import BaseModel


class Comment(BaseModel):

    # - - - - - - -
    # config model |
    # - - - - - - -

    # Stream status change
    STATUS_ACTIVATED = 'activated'
    STATUS_IDLE = 'idle'

    # User status change
    STATUS_JOINED = 'joined'
    STATUS_LEFT = 'left'

    # User comment posted
    STATUS_LOW = 'low'
    STATUS_MID_LOW = 'mid_low'
    STATUS_NEUTRAL = 'neutral'
    STATUS_MID_HIGH = 'mid_high'
    STATUS_HIGH = 'high'

    # Playback change
    STATUS_SPIN = 'spin'
    STATUS_STOP = 'stop'
    STATUS_START = 'start'
    STATUS_PLAY = 'play'
    STATUS_PAUSE = 'pause'
    STATUS_NEXT = 'next'
    STATUS_PREV = 'prev'

    STATUS_CHOICES = [
        (STATUS_JOINED, 'Joined'),
        (STATUS_LEFT, 'Left'),
        (STATUS_ACTIVATED, 'Activated'),
        (STATUS_IDLE, 'Idle'),
        (STATUS_LOW, ':('),
        (STATUS_MID_LOW, ':/'),
        (STATUS_NEUTRAL, ':|'),
        (STATUS_MID_HIGH, ':)'),
        (STATUS_HIGH, ':D'),
        (STATUS_SPIN, 'Spinning'),
        (STATUS_STOP, 'Stopped'),
        (STATUS_START, 'Started'),
        (STATUS_PLAY, 'Played'),
        (STATUS_PAUSE, 'Paused'),
        (STATUS_NEUTRAL, 'Neutral'),
        (STATUS_NEXT, 'Skipped'),
        (STATUS_PREV, 'Backtracked'),
    ]

    class Meta:
        abstract = False

    objects = CommentManager.from_queryset(CommentQuerySet)()

    def __str__(self):
        return f'[{self.commenter_id}] {self.text}'

    # - - - -
    # fields |
    # - - - -

    created_at = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    text = models.TextField(null=True, blank=True)

    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.DO_NOTHING,
        null=True,
    )
    commenter_ticket = models.ForeignKey(
        'music.Ticket',
        related_name='commenter_tickets',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    stream = models.ForeignKey(
        'music.Stream', related_name='comments', on_delete=models.DO_NOTHING,
    )
    record = models.ForeignKey(
        'music.Record', related_name='spins', on_delete=models.SET_NULL, null=True,
    )
    track = models.ForeignKey(
        'music.Track',
        related_name='comments',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_timestamp = models.DurationField(null=True, blank=True)
