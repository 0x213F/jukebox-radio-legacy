
from django.contrib import admin
from django.urls import path

from .views import home_view
from .views import play_view
from .views import index_view
from .views import privacy_policy_view

urlpatterns = [
    path('', index_view),
    path('home/', home_view),
    path('play/<uuid>/', play_view),
    path('privacy-policy/', privacy_policy_view),
]
