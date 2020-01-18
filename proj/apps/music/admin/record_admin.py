
import requests
from datetime import datetime
from datetime import timedelta

from django import forms
from django import urls
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.conf.urls import url
from django.shortcuts import redirect

from proj.apps.music.admin.inline import TrackInline
from proj.apps.music.forms import RecordForm
from proj.apps.music.models import Comment
from proj.apps.music.models import Record
from proj.apps.music.models import TrackListing
from proj.apps.music.models import Track
from proj.apps.music.backends import Spotify
from proj.apps.users.models import Profile



@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^link-spotify/$', self.link_spotify, name="link_spotify")
        ]
        return my_urls + urls

    # - - - - -
    # display
    # - - - - -

    change_list_template = 'admin/track_change_list.html'

    form = RecordForm

    search_fields = (
        'id',
        'name__icontains',
    )

    list_display = (
        'name',
        'display_tracks',
        'duration',
    )

    readonly_fields = (
        'display_tracks',
        'duration',
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.fields = (
                'name',
            )
        else:
            self.fields = (
                'name',
                'display_tracks',
                'duration',
            )
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('id')

    def display_tracks(self, record):
        track_listings = (
            TrackListing
            .objects
            .filter(record=record)
            .order_by('number')
        )

        # if the record has already been played once, do not allow it to be
        # editable.
        not_is_editable = Comment.objects.filter(record=record).exists()

        track_str = ''
        for tl in track_listings:
            track = tl.track
            track_link = urls.reverse(
                'admin:music_track_change', args=[track.id]
            )
            track_listing_link = urls.reverse(
                'admin:music_tracklisting_delete', args=[tl.id]
            )
            track_str += f'<button><a href="{track_link}">🔗 {track.spotify_name}</a></button>'

            # is editable
            if not not_is_editable:
                track_str += (
                    f'<button><a href="{track_listing_link}">🗑</a></button>'
                )

            track_str += '<div style="height: 0.25rem;"></div>'

        if not_is_editable:
            return format_html(track_str)

        if track_listings:
            track_str += '<div style="height: 0.75rem;"></div>'
        track_link = (
            urls.reverse('admin:music_track_add') +
            f'?record={record.id}'
        )
        track_str += (
            '<button style="font-weight: 800">'
            f'    <a href="{track_link}">🔗 Add Track</a>'
            '</button>'
        )

        return format_html(track_str)

    def duration(self, record):
        return timedelta(seconds=(record.duration_ms / 1000))

    def link_spotify(self, request):
        Profile.objects.get_or_create(user=request.user)
        spotify_authorization_uri = Spotify.get_spotify_authorization_uri(request, 'admin')
        return redirect(spotify_authorization_uri)
