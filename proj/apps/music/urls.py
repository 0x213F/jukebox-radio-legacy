from django.urls import path

from .views import CreateStreamView
from .views import ListBroadcastingStreamsView
from .views import ListRecordsView
from .views import ListStreamsView
from .views import SpinRecordView
from .views import StreamSubscriptionView
from .views import UpdateStreamView


urlpatterns = [
    path("create_stream/", CreateStreamView.as_view()),
    path("list_broadcasting_streams/", ListBroadcastingStreamsView.as_view()),
    path("list_records/", ListRecordsView.as_view()),
    path("list_streams/", ListStreamsView.as_view()),
    path("spin_record/", SpinRecordView.as_view()),
    path("stream_subscription/", StreamSubscriptionView.as_view()),
    path("update_stream/", UpdateStreamView.as_view()),
]
