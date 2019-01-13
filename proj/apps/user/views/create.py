
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse

from proj.apps.user.forms import UserForm

User = get_user_model()


def create_view(request):

    # user must be logged out to create a user
    if request.user.is_authenticated:
        return HttpResponse(status=403)

    # required params
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if not (username and password):
        return HttpResponse(status=400)

    # semi-optional params
    email = request.POST.get('email', None)
    phone = request.POST.get('phone', None)
    if (not email) and (not phone):
        return HttpResponse(status=400)
    elif email:
        pass  # TODO send email verification
    elif phone:
        pass  # TODO send phone verficiation

    # verify the username doesn't already exist
    if User.objects.filter(username=username).count():
        return HttpResponse(status=400)

    # create user
    user = User.objects.create_user(
        username,
        password=password,
        email=email,
        phone=phone,
    )
    login(request, user)
    return HttpResponse(status=201)
