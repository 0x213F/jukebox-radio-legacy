
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.music.models.managers import ArtistManager
from proj.apps.music.models.querysets import ArtistQuerySet

from proj.core.models import BaseModel


class Artist(BaseModel):

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = ArtistManager.from_queryset(ArtistQuerySet)()

    # - - - -
    # fields
    # - - - -

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
