
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import home_view
from .views import play_view
from .views import index_view
from .views import privacy_policy_view


urlpatterns = [
    path('', index_view),
    path('home/', home_view),
    path('play/', play_view),
    path('privacy-policy/', privacy_policy_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
