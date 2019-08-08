
from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import ConnectView
from .views import index_view


urlpatterns = [
    path('', index_view),
    path('connect/', ConnectView.as_view()),
]
