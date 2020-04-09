from datetime import datetime

from django import forms
from django.contrib import admin
from django.contrib import messages
from django import urls
from django.utils.html import format_html

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    ChoiceDropdownFilter,
    RelatedDropdownFilter,
)

from proj.apps.music.models import Comment
from proj.apps.music.models import Record
from proj.apps.music.models import Stream
from proj.apps.music.models import TrackListing

from proj.apps.music.forms import StreamForm


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):

    # - - - - -
    # display
    # - - - - -

    form = StreamForm

    search_fields = (
        "id",
        "uuid",
        "title",
        "status__icontains",
    )

    list_display = (
        "title",
        "record",
        "tracks",
        "time_left",
        "status",
        "comments",
    )

    list_filter = (("status", DropdownFilter),)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")

    def link_to_record(self, stream):
        record = stream.current_record
        record_link = urls.reverse("admin:music_record_change", args=[record.id])
        return format_html(
            f'<button><a href="{record_link}">{record.name}</a></button>'
        )

    def time_left(self, stream):
        return stream.time_left_on_current_record

    def record(self, stream):
        record = stream.current_record
        if not record:
            return None
        track_link = urls.reverse("admin:music_record_change", args=[record.id])
        return format_html(
            f'<button><a href="{track_link}">🔗 {record.name}</a></button>'
            '<div style="height: 0.25rem;"></div>'
        )

    def tracks(self, stream):
        if not stream.time_left_on_current_record:
            return None
        now = datetime.now()
        record = stream.current_record
        track_listings = TrackListing.objects.filter(record=record).order_by("number")

        now_playing = (
            Comment.objects.filter(
                created_at__lte=now, stream=stream, status=Comment.STATUS_START,
            )
            .order_by("-created_at")
            .first()
        )
        now_track = now_playing.track

        track_str = ""
        for tl in track_listings:
            track = tl.track
            track_link = urls.reverse("admin:music_track_change", args=[track.id])
            if track.id == now_track.id:
                track_str += (
                    f'<button><a href="{track_link}" style="font-style: oblique;">🔗 {track.spotify_name}</a></button>'
                    '<div style="height: 0.25rem;"></div>'
                )
            else:
                track_str += (
                    f'<button><a href="{track_link}">🔗 {track.spotify_name}</a></button>'
                    '<div style="height: 0.25rem;"></div>'
                )

        return format_html(track_str)

    def comments(self, stream):
        record = stream.current_record
        record_link = urls.reverse("admin:music_comment_changelist")
        return format_html(
            f"<button>"
            f'<a href="{record_link}?stream__id__exact={stream.id}">'
            f"🔗 Comments"
            "</a>"
            "</button>"
        )
