from django import forms

from proj.apps.music.models import Record
from proj.apps.music.models import Track


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ("name",)
