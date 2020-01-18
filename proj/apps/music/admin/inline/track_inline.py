from django import urls
from django.contrib import admin
from django.utils.html import format_html

from proj.apps.music.models import Track


class TrackInline(admin.TabularInline):
    """

    """

    model = Track

    # - - - - - - -
    # permissions
    # - - - - - - -

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    # - - - - -
    # display
    # - - - - -

    fields = (
        "spotify_name",
        "spotify_uri",
        "track_length",
        "link_to_track",
    )
    readonly_fields = (
        "spotify_uri",
        "spotify_name",
        "track_length",
        "link_to_track",
    )
    extra = 0

    def track_length(self, track):
        total_seconds = track.spotify_duration_ms / 1000
        minutes = int(total_seconds / 60)
        seconds = int(total_seconds) % 60
        return f"{minutes}:{seconds:02}"

    def link_to_track(self, track):
        link = urls.reverse("admin:music_track_change", args=[track.id])
        return format_html(f'<a href="{link}">●●●►</a>')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")
