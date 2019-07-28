
from datetime import datetime

from django import forms
from django.contrib import admin

from proj.apps.music.models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass
