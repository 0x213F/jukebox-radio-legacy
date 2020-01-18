from cryptography.fernet import Fernet
from datetime import datetime
import requests

from django.conf import settings
from django import urls
from django.apps import apps
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.conf.urls import url
from django.shortcuts import redirect

from proj.apps.music.forms import TrackForm
from proj.apps.music.models import TrackListing
from proj.apps.music.models import Track
from proj.apps.music.backends import Spotify
from proj.apps.users.models import Profile


@admin.register(TrackListing)
class TrackListingAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("record_id", "number")
