
import requests

from datetime import datetime

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

from proj.apps.music.models import Track


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('record', 'value', 'spotify_uri',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    form = TrackForm

    def save_model(self, request, obj, form, change):
        '''
        '''
        spotify_id =  obj.spotify_uri[14:]
        spotify_access_token = (
            User
            .objects
            .get(email__iexact='josh@schultheiss.io')
            .profile
            .spotify_access_token
        )

        response = requests.get(
            f'https://api.spotify.com/v1/tracks/{spotify_id}',
            headers={
                'Authorization': f'Bearer {spotify_access_token}',
                'Content-Type': 'application/json',
            },
        )
        response_json = response.json()

        obj.spotify_name = response_json['name']
        obj.spotify_duration_ms = response_json['duration_ms']

        super().save_model(request, obj, form, change)
