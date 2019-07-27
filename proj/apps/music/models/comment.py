
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

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = CommentManager.from_queryset(CommentQuerySet)()

    STATUS_WAITING = 'waiting'
    STATUS_LOW = 'low'
    STATUS_MID_LOW = 'mid_low'
    STATUS_MID_HIGH = 'mid_high'
    STATUS_HIGH = 'high'

    # - - - -
    # fields
    # - - - -

    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    text = models.FloatField()

    status = models.FloatField()

    showing = models.ForeignKey(
        'music.Showing',
        related_name='comments',
        on_delete=models.DO_NOTHING,
    )

    timestamp = models.FloatField()

    track = models.CharField(editable=False, max_length=128)
