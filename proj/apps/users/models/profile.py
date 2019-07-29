
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from .managers import ProfileManager
from .querysets import ProfileQuerySet

from proj.core.models import BaseModel


class Profile(BaseModel):

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = ArtistManager.from_queryset(ArtistQuerySet)()

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
    display_name = models.CharField(max_length=32, null=True, blank=True)
    showing_uuid = models.CharField(max_length=64, null=True, blank=True)
