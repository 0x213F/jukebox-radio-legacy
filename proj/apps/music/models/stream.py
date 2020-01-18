import uuid

from datetime import datetime
from datetime import timezone

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from proj.apps.music.models.managers import StreamManager
from proj.apps.music.models.querysets import StreamQuerySet

from proj.core.models import BaseModel


class Stream(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    STATUS_ACTIVATED = "activated"
    STATUS_IDLE = "idle"

    STATUS_CHOICES = [
        (STATUS_ACTIVATED, "Activated"),
        (STATUS_IDLE, "idle"),
    ]

    class Meta:
        abstract = False

    objects = StreamManager.from_queryset(StreamQuerySet)()

    def __str__(self):
        return self.title

    # - - - -
    # fields
    # - - - -

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=128)  # name

    current_record = models.ForeignKey(
        "music.Record",
        related_name="now_playing_at_streams",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    showtime_actual = models.DateTimeField(null=True, blank=False)

    last_status_change_at = models.DateTimeField(null=True, blank=True)
    record_terminates_at = models.DateTimeField(null=True, blank=False)

    status = models.CharField(max_length=128, default=STATUS_IDLE)

    @property
    def chat_room(self):
        # TODO need a more graceful way of doing this with async. for now a
        # constant is fine
        # foo = ContentType.objects.get_for_model(self)
        foo = 1
        return f"{foo}-{self.id}"

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
