
from django import forms

from proj.apps.music.models import Record
from proj.apps.music.models import Stream


class StreamForm(forms.ModelForm):

    next_record = forms.ModelChoiceField(
        queryset=Record.objects.all(),
        required=False,
    )

    class Meta:
        model = Stream
        fields = (
            'title',
            'next_record',
        )
