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

    # User status change
    STATUS_JOINED = "joined"
    STATUS_LEFT = "left"

    # User comment posted
    STATUS_COMMENTED = "comment"

    STATUS_CHOICES = [
        (STATUS_JOINED, "Joined"),
        (STATUS_LEFT, "Left"),
        (STATUS_COMMENTED, "Commented"),
    ]

    class Meta:
        abstract = False

    objects = CommentManager.from_queryset(CommentQuerySet)()

    def __str__(self):
        if self.status == self.STATUS_COMMENTED:
            return f"[{self.commenter_id}] {self.text}"
        else:
            return f"[{self.commenter_id}] {self.status}"

    # - - - -
    # fields |
    # - - - -

    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    text = models.TextField(null=True, blank=True)

    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    commenter_ticket = models.ForeignKey(
        "music.Ticket",
        related_name="commenter_tickets",
        on_delete=models.DO_NOTHING,
        null=True,
    )

    stream = models.ForeignKey(
        "music.Stream", related_name="comments", on_delete=models.DO_NOTHING,
    )
    record = models.ForeignKey(
        "music.Record", related_name="spins", on_delete=models.SET_NULL, null=True,
    )
    track = models.ForeignKey(
        "music.Track",
        related_name="comments",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_timestamp = models.DurationField(null=True, blank=True)
