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

    list_filter = (
        # for related fields
        ("status", DropdownFilter),
    )

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.fields = ("title",)
            self.readonly_fields = ("",)
        elif obj.status == Stream.STATUS_IDLE:
            self.fields = ("title", "vote_controlled")
            self.readonly_fields = ("",)
        elif obj.status == Stream.STATUS_ACTIVATED:
            if obj.time_left_on_current_record:
                self.fields = (
                    "title",
                    "link_to_record",
                    "tracks",
                    "time_left",
                    "record_terminates_at",
                )
                self.readonly_fields = (
                    "link_to_record",
                    "tracks",
                    "time_left",
                    "record_terminates_at",
                )
            else:
                self.fields = (
                    "title",
                    "next_record",
                    "time_left",
                    "record_terminates_at",
                )
                self.readonly_fields = (
                    "title",
                    "link_to_record",
                    "time_left",
                    "record_terminates_at",
                )
        return super().get_form(request, obj, **kwargs)

    # inlines = [
    #     RecordInline,
    # ]

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

    # - - - - -
    # actions
    # - - - - -

    actions = [
        "activate_selected_stream",
        "idle_selected_stream",
    ]

    def activate_selected_stream(self, request, queryset):
        scheduled = queryset.filter(status__in=(Stream.STATUS_IDLE,))
        if queryset.count() != scheduled.count():
            self.message_user(
                request, "Make sure all streams are scheduled.", level=messages.ERROR,
            )
            return
        for stream in queryset:
            Stream.objects.change_status(stream, Stream.STATUS_ACTIVATED)

    activate_selected_stream.short_description = "Activate selected stream"

    def idle_selected_stream(self, request, queryset):
        scheduled = queryset.filter(status__in=(Stream.STATUS_ACTIVATED))
        if queryset.count() != scheduled.count():
            self.message_user(
                request, "Make sure all streams are activated.", level=messages.ERROR,
            )
            return
        for stream in queryset:
            Stream.objects.change_status(stream, Stream.STATUS_IDLE)

    idle_selected_stream.short_description = "Idle selected stream"

    # - - -
    # save
    # - - -

    def save_model(self, request, stream, form, change):
        """
        Cache data from Spotify API.
        """
        now = datetime.now()
        try:
            pre_save_stream = Stream.objects.get(id=stream.id)
            if pre_save_stream.current_record and pre_save_stream.record_terminates_at:
                if now < pre_save_stream.record_terminates_at.replace(tzinfo=None):
                    self.message_user(
                        request,
                        "The record cannot be changed since one is still playing.",
                        level=messages.ERROR,
                    )
                    return
        except Stream.DoesNotExist:
            pass

        next_record = form.cleaned_data["next_record"]

        super().save_model(request, stream, form, change)

        if not next_record:
            return

        Stream.objects.spin(next_record, stream)
