from django.urls import path

from .views import signin_view
from .views import signout_view
from .views import signup_view
from .views import UpdateView


urlpatterns = [
    path('signin/', signin_view),
    path('signout/', signout_view),
    path('signup/', signup_view),
    path('update/', UpdateView.as_view()),
]
