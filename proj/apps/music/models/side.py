
from django.contrib.postgres.fields import ArrayField
from django.db import models

from proj.apps.music.models.managers import SideManager
from proj.apps.music.models.querysets import SideQuerySet

from proj.core.models import BaseModel


class Side(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False

    objects = SideManager.from_queryset(SideQuerySet)()

    # def __str__(self):
    #     return 'TODO'

    # - - - - - - - - -
    # fields
    # - - - - - - - - -

    number = models.PositiveIntegerField()

    track_0 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track0',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_1 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track1',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_2 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track2',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_3 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track3',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_4 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track4',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_5 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track5',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_6 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track6',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_7 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track7',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_8 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track8',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    track_9 = models.ForeignKey(
        'music.Track',
        related_name='sides_with_track9',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
