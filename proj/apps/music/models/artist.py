
from django.conf import settings
from django.db import models

from proj.apps.music.models.managers import ArtistManager
from proj.apps.music.models.querysets import ArtistQuerySet

from proj.core.models import BaseModel


class Artist(BaseModel):

    # - - - - - - -
    # config model
    # - - - - - - -

    class Meta:
        abstract = False

    objects = ArtistManager.from_queryset(ArtistQuerySet)()

    def __str__(self):
        return self.full_name


    # - - - -
    # fields
    # - - - -

    full_name = models.CharField(max_length=128)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='artist',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
