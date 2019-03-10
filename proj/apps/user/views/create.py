
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse

from proj.apps.user.forms import UserForm

User = get_user_model()


def create_view(request):

    # authentication
    # - - - - - - - -
    if request.user.is_authenticated:
        return HttpResponse(status=403)


    # form validation
    # - - - - - - - -
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if not username or not password:
        return HttpResponse(status=400)

    email_addr = request.POST.get('email', None)
    phone_num = request.POST.get('phone', None)
    if (not email_addr) and (not phone_num):
        return HttpResponse(status=400)

    # verify
    # - - - - - -
    Email.verify(email_addr) if email_addr else SMS.verify(phone_num)

    # create
    # - - - -
    try:
        user = User.objects.create_user(
            username,
            password=password,
            email=email,
            phone=phone,
        )
        login(request, user)
        return HttpResponse(status=201)
    except Exception:
        return HttpResponse(status=400)
