
import json
from datetime import datetime

from django import forms
from django.contrib import admin

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from proj.apps.music.models import Showing


class ShowingForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = (
            'album',
            'scheduled_showtime'
        )


@admin.register(Showing)
class ShowingAdmin(admin.ModelAdmin):
    form = ShowingForm

    actions = ['start_show', 'complete_show', 'terminate_show']

    def save_model(self, request, obj, form, change):
        if not change:
            album = form.cleaned_data['album']
            scheduled_showing_exists = (
                Showing.objects
                .filter(album=album, status=Showing.STATUS_SCHEDULED).exists()
            )
            if scheduled_showing_exists:
                return  # TODO add error message
        super().save_model(request, obj, form, change)

    def start_show(self, request, queryset):
        scheduled = queryset.filter(status=Showing.STATUS_SCHEDULED)
        if queryset.count() != scheduled.count():
            return
        queryset.update(
            actual_showtime=datetime.now(),
            status=Showing.STATUS_ACTIVE,
        )
        channel_layer = get_channel_layer()
        for showing in queryset:
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            async_to_sync(channel_layer.group_send)(
                showing.chat_room,
                {
                    'type': 'broadcast',
                    'text': json.dumps({
                        'system': {
                            'message': 'start',
                            'sent_at': now,
                        }
                    }),
                }
            )
    start_show.short_description = "Start the show"

    def complete_show(self, request, queryset):
        already_completed = queryset.filter(status=Showing.STATUS_COMPLETE)
        if already_completed.exists():
            return
        queryset.update(
            actual_showtime=datetime.now(),
            status=Showing.STATUS_COMPLETE,
        )
        channel_layer = get_channel_layer()
        for showing in queryset:
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            async_to_sync(channel_layer.group_send)(
                showing.chat_room,
                {
                    'type': 'broadcast',
                    'text': json.dumps({
                        'system': {
                            'message': Showing.STATUS_COMPLETE,
                            'sent_at': now,
                        }
                    }),
                }
            )
    start_show.short_description = "Start the show"

    def terminate_show(self, request, queryset):
        already_terminated = queryset.filter(status=Showing.STATUS_TERMINATED)
        if already_terminated.exists():
            return
        queryset.update(
            actual_showtime=datetime.now(),
            status=Showing.STATUS_TERMINATED,
        )
        channel_layer = get_channel_layer()
        for showing in queryset:
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            async_to_sync(channel_layer.group_send)(
                showing.chat_room,
                {
                    'type': 'broadcast',
                    'text': json.dumps({
                        'system': {
                            'message': Showing.STATUS_TERMINATED,
                            'sent_at': now,
                        }
                    }),
                }
            )
    terminate_show.short_description = "Terminate the show"
