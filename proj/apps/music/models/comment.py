
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
    STATUS_WAITING = 'waiting'
    STATUS_LEFT = 'left'

    STATUS_LOW = 'low'
    STATUS_MID_LOW = 'mid_low'
    STATUS_MID_HIGH = 'mid_high'
    STATUS_HIGH = 'high'

    class Meta:
        abstract = False

    objects = CommentManager.from_queryset(CommentQuerySet)()

    def __str__(self):
        return f'[{self.commenter_id}] {self.text}'

    # - - - -
    # fields
    # - - - -

    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    text = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=128)

    showing = models.ForeignKey(
        'music.Showing',
        related_name='comments',
        on_delete=models.DO_NOTHING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    timestamp = models.FloatField()

    track = models.ForeignKey(
        'music.Track',
        related_name='comments',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
