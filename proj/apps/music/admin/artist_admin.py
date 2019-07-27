
from django.contrib import admin

from proj.apps.music.models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass
