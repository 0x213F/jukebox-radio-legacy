from django import urls
from django.contrib import admin
from django.utils.html import format_html

from proj.apps.music.models import TrackListing
from proj.apps.music.models import Record


class RecordInline(admin.TabularInline):
    """
    """

    model = Record

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
        "name",
        "record_length",
        "track_count",
        "is_playing",
        "link_to_record",
    )
    readonly_fields = (
        "name",
        "record_length",
        "track_count",
        "is_playing",
        "link_to_record",
    )
    extra = 0

    def record_length(self, record):
        track_durations = TrackListing.objects.filter(record=record).values_list(
            "track__spotify_duration_ms", flat=True
        )
        total_seconds = sum(track_durations) / 1000
        minutes = int(total_seconds / 60)
        seconds = int(total_seconds) % 60
        return f"{minutes}:{seconds:02}"

    def track_count(self, record):
        return TrackListing.objects.filter(record=record).count()

    def link_to_record(self, record):
        link = urls.reverse("admin:music_record_change", args=[record.id])
        return format_html(f'<a href="{link}">●●●►</a>')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")
