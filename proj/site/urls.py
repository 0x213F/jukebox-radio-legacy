from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import AccountView
from .views import ConnectView
from .views import CreateStreamView
from .views import IndexView
from .views import LinkSpotifyView
from .views import SignInView
from .views import SignUpView
from .views import StreamView


urlpatterns = [
    path('', IndexView.as_view()),
    path('account/', AccountView.as_view()),
    path('connect/', ConnectView.as_view()),
    path('createstream/', CreateStreamView.as_view()),
    path('login/', SignInView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('linkspotify/', LinkSpotifyView.as_view()),
    path('stream/<stream>/', StreamView.as_view()),
]
