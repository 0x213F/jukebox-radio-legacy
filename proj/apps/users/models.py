
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

# from proj.apps.music.models.managers import ArtistManager
# from proj.apps.music.models.querysets import ArtistQuerySet

from proj.core.models import BaseModel


class Profile(BaseModel):

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    # objects = ArtistManager.from_queryset(ArtistQuerySet)()

    # - - - -
    # fields
    # - - - -

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.DO_NOTHING,
    )

    active_showing = models.ForeignKey(
        'music.Showing',
        related_name='active_users',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
