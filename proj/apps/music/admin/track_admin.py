from cryptography.fernet import Fernet
from datetime import datetime
import requests

from django.conf import settings
from django import urls
from django.apps import apps
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.conf.urls import url
from django.shortcuts import redirect

from proj.apps.music.forms import TrackForm
from proj.apps.music.models import TrackListing
from proj.apps.music.models import Track
from proj.apps.users.models import Profile
from proj.core.resources import Spotify


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [url(r"^link-spotify/$", self.link_spotify, name="link_spotify")]
        return my_urls + urls

    # - - - - -
    # display
    # - - - - -

    change_list_template = "admin/track_change_list.html"

    form = TrackForm

    search_fields = (
        "spotify_uri__exact",
        "spotify_name__icontains",
        "record__name__icontains",
    )

    list_display = (
        "name",
        "records",
        "spotify_uri",
        "track_length",
        "comments",
    )

    readonly_fields = (
        "records",
        "spotify_name",
        "track_length",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("id")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.fields = (
                "spotify_uri",
                "record",
            )
        else:
            self.fields = (
                ("spotify_name", "track_length"),
                "records",
            )
        return super().get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return False

    def name(self, track):
        return track.spotify_name

    def comments(self, track):
        track_link = urls.reverse("admin:music_comment_changelist")
        return format_html(
            f"<button>"
            f'<a href="{track_link}?track__id__exact={track.id}">'
            f"🔗 Comments"
            "</a>"
            "</button>"
        )

    def records(self, track):
        track_listings = TrackListing.objects.filter(track=track).order_by("number")

        records_str = ""
        for tl in track_listings:
            record = tl.record
            record_link = urls.reverse("admin:music_record_change", args=[record.id])
            records_str += (
                f'<button><a href="{record_link}">🔗 {record.name}</a></button>'
                '<div style="height: 0.25rem;"></div>'
            )

        return format_html(records_str)

    def track_length(self, track):
        total_seconds = track.spotify_duration_ms / 1000
        minutes = int(total_seconds / 60)
        seconds = int(total_seconds) % 60
        return f"{minutes}:{seconds:02}"

    # - - -
    # save
    # - - -

    def save_model(self, request, track, form, change):
        """
        Cache data from Spotify API.
        """
        Record = apps.get_model("music.Record")

        record = form.cleaned_data["record"]
        spotify_uri = form.cleaned_data["spotify_uri"]

        try:
            track_that_already_exists = Track.objects.get(spotify_uri=spotify_uri)
            if track_that_already_exists:
                track = track_that_already_exists
                number = TrackListing.objects.filter(record=record).count() + 1
                TrackListing.objects.create(
                    record=record, track=track, number=number,
                )
                return
        except Exception:
            pass

        cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)
        spotify_access_token = cipher_suite.decrypt(
            request.user.profile.spotify_access_token.encode("utf-8")
        ).decode("utf-8")
        spotify_id = track.spotify_uri[14:]

        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{spotify_id}",
            headers={
                "Authorization": f"Bearer {spotify_access_token}",
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        spotify_duration_ms = response_json["duration_ms"]
        track.spotify_duration_ms = spotify_duration_ms

        track.spotify_name = response_json["name"][:32]
        if len(response_json["name"]) > 32:
            track.spotify_name += "..."

        super().save_model(request, track, form, change)

        if not record:
            return

        number = TrackListing.objects.filter(record=record).count() + 1

        TrackListing.objects.create(
            record=record, track=track, number=number,
        )

    def link_spotify(self, request):
        Profile.objects.get_or_create(user=request.user)
        spotify_authorization_uri = Spotify.get_spotify_authorization_uri(
            request, "admin"
        )
        return redirect(spotify_authorization_uri)
