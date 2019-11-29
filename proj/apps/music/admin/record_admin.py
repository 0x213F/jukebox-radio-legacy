
from datetime import datetime

from django import forms
from django.contrib import admin

from proj.apps.music.models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('showing', 'tracks',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    form = RecordForm

    actions = ['spin', 'play', 'pause']

    def spin(self, request, queryset):
        still = queryset.filter(played_at__isnull=True)
        if queryset.count() != still.count():
            return
        for record in queryset:
            Record.objects.spin(record)
    spin.short_description = "Spin the record"

    def play(self, request, queryset):
        unplayed = queryset.filter(played_at__isnull=False, is_playing=False)
        if queryset.count() != unplayed.count():
            return
        for record in queryset:
            Record.objects.play(record)
    play.short_description = "Play the record"

    def pause(self, request, queryset):
        playing = queryset.filter(played_at__isnull=False, is_playing=True)
        if queryset.count() != playing.count():
            return
        for record in queryset:
            Record.objects.pause(record)
    pause.short_description = "Pause the record"
