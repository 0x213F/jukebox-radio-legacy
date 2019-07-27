
from django.contrib import admin

from proj.apps.music.models import Album


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
