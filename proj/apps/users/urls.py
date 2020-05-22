from django.urls import path

from .views import UpdateView, signin_view, signout_view, signup_view

urlpatterns = [
    path("signin/", signin_view),
    path("signout/", signout_view),
    path("signup/", signup_view),
    path("update/", UpdateView.as_view()),
]
