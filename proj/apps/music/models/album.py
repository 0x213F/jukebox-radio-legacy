
from django.db import models

from proj.apps.music.models.managers import AlbumManager
from proj.apps.music.models.querysets import AlbumQuerySet

from proj.core.models import BaseModel


class Album(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False

    objects = AlbumManager.from_queryset(AlbumQuerySet)()

    def __str__(self):
        return f'[{self.artist}] {self.title}'

    # - - - - - - - - -
    # fields
    # - - - - - - - - -

    art = models.URLField(max_length=256)
    artist = models.ForeignKey(
        'music.Artist',
        related_name='albums',
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(max_length=128)
    release_date = models.DateField()
