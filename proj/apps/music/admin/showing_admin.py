
from django import forms
from django.contrib import admin

from proj.apps.music.models import Showing


class ShowingForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        album = cleaned_data.get('album')
        scheduled_showing_exists = (
            Showing.objects
            .filter(album=album, status=Showing.STATUS_SCHEDULED).exists()
        )
        if scheduled_showing_exists:
            raise forms.ValidationError(
                'There may only be one scheduled showing per album.'
            )


@admin.register(Showing)
class ShowingAdmin(admin.ModelAdmin):
    form = ShowingForm

    actions = ['start_show']

    def start_show(self, request, queryset):
        queryset.update(status=Showing.STATUS_ACTIVE)
    start_show.short_description = "Start the show"
