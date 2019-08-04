
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.music.models.managers import CommentManager
from proj.apps.music.models.querysets import CommentQuerySet

from proj.core.models import BaseModel


class Comment(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    STATUS_JOINED = 'joined'
    STATUS_WAITED = 'waited'
    STATUS_LEFT = 'left'

    STATUS_ACTIVATED = 'activated'
    STATUS_COMPLETED = 'completed'
    STATUS_TERMINATED = 'terminated'

    STATUS_LOW = 'low'
    STATUS_MID_LOW = 'mid_low'
    STATUS_MID_HIGH = 'mid_high'
    STATUS_HIGH = 'high'

    STATUS_PAUSE = 'pause'
    STATUS_PLAY = 'play'
    STATUS_SKIP_FORWARD = 'skip_forward'

    STATUS_CHOICES = [
        (STATUS_JOINED, 'Joined'),
        (STATUS_WAITED, 'Waited'),
        (STATUS_LEFT, 'Left'),
        (STATUS_ACTIVATED, 'Activated'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_TERMINATED, 'Terminated'),
        (STATUS_LOW, ':('),
        (STATUS_MID_LOW, ':/'),
        (STATUS_MID_HIGH, ':)'),
        (STATUS_HIGH, ':D'),
    ]

    class Meta:
        abstract = False

    objects = CommentManager.from_queryset(CommentQuerySet)()

    def __str__(self):
        return f'[{self.commenter_id}] {self.text}'

    # - - - -
    # fields
    # - - - -

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    text = models.TextField(null=True, blank=True)

    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.DO_NOTHING,
        null=True,
    )
    showing = models.ForeignKey(
        'music.Showing',
        related_name='comments',
        on_delete=models.DO_NOTHING,
    )
    showing_timestamp = models.DurationField()
    track = models.ForeignKey(
        'music.Track',
        related_name='comments',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    track_timestamp = models.DurationField()
