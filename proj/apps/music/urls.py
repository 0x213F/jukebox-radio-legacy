from django.urls import path

from .views import CreateQueueView
from .views import CreateRecordView
from .views import CreateStreamView
from .views import DeleteQueueView
from .views import ListBroadcastingStreamsView
from .views import ListHostsView
from .views import ListQueueView
from .views import ListRecordsView
from .views import ListStreamsView
from .views import SearchLibraryView
from .views import SpinRecordView
from .views import StreamSubscriptionView
from .views import UpdateStreamView
from .views import UpdateTicketView


urlpatterns = [
    path("create_queue/", CreateQueueView.as_view()),
    path("create_record/", CreateRecordView.as_view()),
    path("create_stream/", CreateStreamView.as_view()),
    path("delete_queue/", DeleteQueueView.as_view()),
    path("list_broadcasting_streams/", ListBroadcastingStreamsView.as_view()),
    path("list_hosts/", ListHostsView.as_view()),
    path("list_queue/", ListQueueView.as_view()),
    path("list_records/", ListRecordsView.as_view()),
    path("list_streams/", ListStreamsView.as_view()),
    path("search_library/", SearchLibraryView.as_view()),
    path("spin_record/", SpinRecordView.as_view()),
    path("stream_subscription/", StreamSubscriptionView.as_view()),
    path("update_stream/", UpdateStreamView.as_view()),
    path("update_ticket/", UpdateTicketView.as_view()),
]
