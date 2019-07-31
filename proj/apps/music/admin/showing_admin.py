
from django import forms
from django.contrib import admin

from proj.apps.music.models import Showing


class ShowingForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = ('album', 'showtime_scheduled')


@admin.register(Showing)
class ShowingAdmin(admin.ModelAdmin):
    form = ShowingForm

    actions = ['activate_showing', 'complete_showing', 'terminate_showing']

    def activate_showing(self, request, queryset):
        scheduled = queryset.filter(status=Showing.STATUS_SCHEDULED)
        if queryset.count() != scheduled.count():
            return
        queryset.objects.update(status=Showing.STATUS_ACTIVATED)
    activate_showing.short_description = "Activate the showing"

    def complete_showing(self, request, queryset):
        already_activated = queryset.filter(status=Showing.STATUS_ACTIVE)
        if queryset.count() != already_activated.count():
            return
        queryset.objects.update(status=Showing.STATUS_COMPLETED)
    complete_showing.short_description = "Start the show"

    def terminate_showing(self, request, queryset):
        already_terminated = queryset.filter(status=Showing.STATUS_TERMINATED)
        if already_terminated.exists():
            return
        queryset.objects.update(status=Showing.STATUS_TERMINATED)
    terminate_showing.short_description = "Terminate the show"