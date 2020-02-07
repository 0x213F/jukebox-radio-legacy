from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import ConnectView
from .views import index_view
from .views import SignInView
from .views import SignUpView
from .views import LinkSpotifyView


urlpatterns = [
    path("", index_view),
    path("connect/", ConnectView.as_view()),
    path("linkspotify/", LinkSpotifyView.as_view()),
    path("signin/", SignInView.as_view()),
    path("signup/", SignUpView.as_view()),
]
