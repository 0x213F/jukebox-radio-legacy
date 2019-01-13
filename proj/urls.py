
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic.base import TemplateView
from django.conf import settings

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/user/', include('proj.apps.user.urls')),
    path('', include('proj.site.urls')),
]
