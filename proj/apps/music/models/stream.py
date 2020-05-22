import uuid
from datetime import datetime

from django.conf import settings
from django.db import models

from proj.apps.music.models.managers import StreamManager
from proj.apps.music.models.querysets import StreamQuerySet
from proj.core.models import BaseModel


class Stream(BaseModel):

    # - - - - - - -
    # config model |
    # - - - - - - -

    STATUS_ACTIVATED = "activated"
    STATUS_IDLE = "idle"

    STATUS_CHOICES = [
        (STATUS_ACTIVATED, "Activated"),
        (STATUS_IDLE, "Idle"),
    ]

    class Meta:
        abstract = False

    objects = StreamManager.from_queryset(StreamQuerySet)()

    def __str__(self):
        checked = "x" if self.status == self.STATUS_ACTIVATED else " "
        return f"[{checked}] {self.title}"

    # - - - -
    # fields |
    # - - - -

    unique_custom_id = models.CharField(
        max_length=64, unique=True, blank=True, null=True
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    status = models.CharField(max_length=128, default=STATUS_IDLE)
    title = models.CharField(max_length=128)
    tags = models.CharField(max_length=128)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_streams",
        on_delete=models.DO_NOTHING,
    )
    owner_name = models.CharField(max_length=128)

    is_private = models.BooleanField(default=False)

    current_queue = models.OneToOneField(
        "music.Queue",
        related_name="active_stream",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    current_tracklisting = models.ForeignKey(
        "music.TrackListing",
        related_name="now_playing_tracklisting",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    record_begun_at = models.DateTimeField(null=True, blank=False)
    record_terminates_at = models.DateTimeField(null=True, blank=False)

    played_at = models.DateTimeField(null=True, blank=False)
    paused_at = models.DateTimeField(null=True, blank=False)

    # - - - - - -
    # properties |
    # - - - - - -

    @property
    def chat_room(self):
        return f"stream-{self.id}"

    @property
    def time_left_on_current_record(self):
        dt = self.record_terminates_at
        if not dt:
            return None

        now = datetime.now()
        dt = dt.replace(tzinfo=None)
        if not dt or now >= dt:
            return None
        else:
            return dt - now
