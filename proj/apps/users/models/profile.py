from django.conf import settings
from django.db import models

from .managers import ProfileManager
from .querysets import ProfileQuerySet

from proj.core.models import BaseModel


class Profile(BaseModel):

    # - - - - - - - -
    # config model   |
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = ProfileManager.from_queryset(ProfileQuerySet)()

    def __str__(self):
        return self.default_display_name

    # - - - -
    # fields |
    # - - - -

    last_active_stream_uuid = models.UUIDField(null=True, blank=True)
    active_stream_uuid = models.UUIDField(null=True, blank=True)
    default_display_name = models.CharField(max_length=32, null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.DO_NOTHING,
    )

    spotify_access_token = models.CharField(max_length=500, null=True, blank=True)
    spotify_refresh_token = models.CharField(max_length=500, null=True, blank=True)
    spotify_scope = models.CharField(max_length=500, null=True, blank=True)
