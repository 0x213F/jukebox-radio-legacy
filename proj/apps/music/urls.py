from django.urls import path

from .views import ListStreamsView
from .views import StreamSubscriptionView


urlpatterns = [
    path("list_streams/", ListStreamsView.as_view()),
    path("stream_subscription/", StreamSubscriptionView.as_view()),
]
