
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import index_view
from .views import route_view


urlpatterns = [
    path('', index_view),
    path('<route>/', route_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
