from django.contrib import admin
from django.urls import path

from .views import authenticate_view
from .views import create_view
from .views import logout_view
from .views import UpdateView

urlpatterns = [
    path("authenticate/", authenticate_view),
    path("create/", create_view),
    path("logout/", logout_view),
    path("update/", UpdateView.as_view()),
]
