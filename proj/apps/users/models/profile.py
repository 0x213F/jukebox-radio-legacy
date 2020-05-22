from django.conf import settings
from django.db import models

from proj.apps.users.models.managers import ProfileManager
from proj.apps.users.models.querysets import ProfileQuerySet
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

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.DO_NOTHING,
    )

    default_display_name = models.CharField(max_length=32, null=True, blank=True)

    activated_stream_redirect = models.CharField(max_length=64, null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    spotify_access_token = models.CharField(max_length=500, null=True, blank=True)
    spotify_refresh_token = models.CharField(max_length=500, null=True, blank=True)
    spotify_scope = models.CharField(max_length=500, null=True, blank=True)
