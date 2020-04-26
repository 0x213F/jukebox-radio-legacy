from django.urls import path

from proj.apps.music.views import SearchView
from proj.apps.music.views import StreamView
from proj.apps.music.views.queue import CreateQueueView
from proj.apps.music.views.queue import DeleteQueueView
from proj.apps.music.views.queue import ListQueuesView
from proj.apps.music.views.stream import CreateStreamView
from proj.apps.music.views.stream import DeleteStreamView
from proj.apps.music.views.stream import ListStreamsView
from proj.apps.music.views.stream import UpdateStreamView
from proj.apps.music.views.ticket import ListTicketsView
from proj.apps.music.views.ticket import UpdateTicketView


urlpatterns = [
    path('search/', SearchView.as_view()),
    path('stream/', StreamView.as_view()),

    path('queue/create/', CreateQueueView.as_view()),
    path('queue/delete/', DeleteQueueView.as_view()),
    path('queue/list/', ListQueuesView.as_view()),

    path('stream/create/', CreateStreamView.as_view()),
    path('stream/delete/', DeleteStreamView.as_view()),
    path('stream/list/', ListStreamsView.as_view()),
    path('stream/update/', UpdateStreamView.as_view()),

    path('ticket/list/', ListTicketsView.as_view()),
    path('ticket/update/', UpdateTicketView.as_view()),
]
