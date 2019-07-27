
from django.contrib import admin
from django.urls import path

from .views import ListShowingsView


urlpatterns = [
        path('list_showings/', ListShowingsView.as_view()),
]
