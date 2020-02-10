from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import include
from django.views.generic.base import TemplateView
from django.views.defaults import page_not_found
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path("api/music/", include("proj.apps.music.urls")),
    path("api/user/", include("proj.apps.users.urls")),
    path("favicon.ico/", page_not_found, {"exception": Exception("Not Found")}),
    path("", include("proj.site.urls")),
    path("admin/", admin.site.urls),
    url(r'^/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
