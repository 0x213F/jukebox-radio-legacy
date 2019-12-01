
from django import forms

from proj.apps.music.models import Record
from proj.apps.music.models import Track


class TrackForm(forms.ModelForm):

    record = forms.ModelChoiceField(
        queryset=Record.objects.all(),
    )

    class Meta:
        model = Track
        fields = (
            'spotify_uri',
            'record',
        )
