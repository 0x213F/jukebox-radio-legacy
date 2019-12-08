
from django.urls import path

from .views import ListShowingsView
from .views import ShowingSubscriptionView


urlpatterns = [
        path('list_showings/', ListShowingsView.as_view()),
        path('showing_subscription/', ShowingSubscriptionView.as_view()),
]
