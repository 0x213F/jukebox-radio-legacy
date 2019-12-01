
from datetime import datetime
import requests

from django import forms
from django import urls
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from proj.apps.music.admin.inline import TrackInline
from proj.apps.music.forms import RecordForm
from proj.apps.music.models import Record
from proj.apps.music.models import TrackListing
from proj.apps.music.models import Track



@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

    # - - - - -
    # display
    # - - - - -

    form = RecordForm

    search_fields = (
        'id',
        'name__icontains',
    )

    list_display = (
        'name',
        'display_tracks',
        'is_playing',
    )

    readonly_fields = (
        'display_tracks',
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

        track_str = ''
        for tl in track_listings:
            track = tl.track
            track_link = urls.reverse(
                'admin:music_track_change', args=[track.id]
            )
            track_str += (
                f'<button><a href="{track_link}">{track.spotify_name}</a></button>'
                '<div style="height: 0.25rem;"></div>'
            )

        if track_listings:
            track_str += '<div style="height: 0.75rem;"></div>'
        track_link = (
            urls.reverse('admin:music_track_add') +
            f'?record={record.id}'
        )
        track_str += (
            '<button style="font-weight: 800">'
            f'    <a href="{track_link}">Add Track</a>'
            '</button>'
        )

        return format_html(track_str)
