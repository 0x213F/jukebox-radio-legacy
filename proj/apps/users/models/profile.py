
from django.conf import settings
from django.db import models

from .managers import ProfileManager
from .querysets import ProfileQuerySet

from proj.core.models import BaseModel


class Profile(BaseModel):

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = ProfileManager.from_queryset(ProfileQuerySet)()

    # - - - -
    # fields
    # - - - -

    active_showing_uuid = models.UUIDField(null=True, blank=True)
    display_name = models.CharField(max_length=32, null=True, blank=True)
    display_uuid = models.UUIDField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.DO_NOTHING,
    )
