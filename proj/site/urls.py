from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import AccountView
from .views import AddRecordView
from .views import ConnectView
from .views import CreateStreamView
from .views import DisplayNameView
from .views import HostsView
from .views import index_view
from .views import QueueView
from .views import RecordsListView
from .views import SignInView
from .views import SignUpView
from .views import StreamView


urlpatterns = [
    path("", index_view),
    path("account/", AccountView.as_view()),
    path("connect/", ConnectView.as_view()),
    path("createstream/", CreateStreamView.as_view()),
    path("login/", SignInView.as_view()),
    path("record/add/", AddRecordView.as_view()),
    path("record/list/", RecordsListView.as_view()),
    path("signup/", SignUpView.as_view()),
    path("stream/<uuid:stream>/", StreamView.as_view()),
    path("stream/<uuid:stream>/manage/", HostsView.as_view()),
    path("stream/<uuid:stream>/queue/", QueueView.as_view()),
    path("stream/<uuid:stream>/displayname/", DisplayNameView.as_view()),
]
