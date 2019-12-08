
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
    default_display_name = models.CharField(max_length=32, null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.DO_NOTHING,
    )

    # TODO: apple_music related fields

    spotify_access_token = models.CharField(max_length=258, null=True, blank=True)
    spotify_refresh_token = models.CharField(max_length=234, null=True, blank=True)
    spotify_scope = models.CharField(max_length=208, null=True, blank=True)
