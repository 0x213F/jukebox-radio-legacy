
from django.contrib.postgres.fields import JSONField
from django.db import models

from proj.apps.music.models.managers import RecordManager
from proj.apps.music.models.querysets import RecordQuerySet

from proj.core.models import BaseModel


class Record(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False
        unique_together = ['showing', 'value']

    objects = RecordManager.from_queryset(RecordQuerySet)()

    def __str__(self):
        try:
            played_at = self.played_at.isoformat()
        except:
            played_at = '<None>'
        return (
            f'<record id="{self.id}" '
            f'value="{self.value}" '
            f'played_at="{played_at}" '
            f'is_playing="{self.is_playing}">"'
        )

    # - - - - - - - - -
    # fields
    # - - - - - - - - -

    played_at = models.DateTimeField(null=True, blank=False)

    is_playing = models.BooleanField(default=False)

    value = models.PositiveIntegerField()

    showing = models.ForeignKey(
        'music.Showing',
        related_name='records',
        on_delete=models.DO_NOTHING,
    )
