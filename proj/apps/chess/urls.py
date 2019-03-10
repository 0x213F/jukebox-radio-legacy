
from django.contrib import admin
from django.urls import path

from .views import create_view
from .views import move_view

urlpatterns = [
    path('create/', create_view),
    path('move/', move_view),
]
