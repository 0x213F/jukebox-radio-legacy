
from django.contrib import admin
from django.urls import path

from .views import do_view
from .views import GetView
from .views import list_view

urlpatterns = [
    path('do/', do_view),
    path('get/', GetView.as_view()),
    path('list/', list_view),
]
