from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import (
    AccountView,
    ConnectView,
    CreateStreamView,
    IndexView,
    LinkSpotifyView,
    SignInView,
    SignUpView,
    StreamView,
)

urlpatterns = [
    path("", IndexView.as_view()),
    path("account/", AccountView.as_view()),
    path("connect/", ConnectView.as_view()),
    path("createstream/", CreateStreamView.as_view()),
    path("login/", SignInView.as_view()),
    path("signup/", SignUpView.as_view()),
    path("linkspotify/", LinkSpotifyView.as_view()),
    path("stream/<stream>/", StreamView.as_view()),
]
