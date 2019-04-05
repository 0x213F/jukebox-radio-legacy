
from django.contrib import admin
from django.urls import path

from .views import create_view
from .views import do_view
from .views import GetView
from .views import list_view

urlpatterns = [
    path('create/', create_view),
    path('do/', do_view),
    path('get/', GetView.as_view()),
    path('list/', list_view),
]
