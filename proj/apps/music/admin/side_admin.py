
from datetime import datetime

from django import forms
from django.contrib import admin

from proj.apps.music.models import Side


@admin.register(Side)
class SideAdmin(admin.ModelAdmin):
    pass
