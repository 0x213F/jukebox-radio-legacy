
from django import forms

from proj.apps.music.models import Record
from proj.apps.music.models import Showing


class ShowingForm(forms.ModelForm):

    current_record = forms.ModelChoiceField(
        queryset=Record.objects.all(),
        required=False,
    )

    class Meta:
        model = Showing
        fields = (
            'title',
            'showtime_scheduled',
            'current_record',
        )
