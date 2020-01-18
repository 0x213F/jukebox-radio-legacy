from django.urls import path

from .views import CreateStreamView
from .views import ListBroadcastingStreamsView
from .views import ListStreamsView
from .views import SpinRecordView
from .views import StreamSubscriptionView


urlpatterns = [
    path("create_stream/", CreateStreamView.as_view()),
    path("list_broadcasting_streams/", ListBroadcastingStreamsView.as_view()),
    path("list_streams/", ListStreamsView.as_view()),
    path("spin_record/", SpinRecordView.as_view()),
    path("stream_subscription/", StreamSubscriptionView.as_view()),
]
