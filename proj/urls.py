
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic.base import TemplateView
from django.views.defaults import page_not_found
from django.conf import settings

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/game/', include('proj.apps.chess.urls')),
    path('api/user/', include('proj.apps.users.urls')),
    path('favicon.ico/', page_not_found, {'exception': Exception('Not Found')}),
    path('', include('proj.site.urls')),
]
