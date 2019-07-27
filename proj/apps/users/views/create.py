
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from random_username.generate import generate_username


@csrf_protect
def create_view(request):

    # authentication
    # - - - - - - - -
    if request.user.is_authenticated:
        return HttpResponse(status=403)


    # form validation
    # - - - - - - - -
    username = generate_username(1)[0]
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if not username or not email or not password:
        return HttpResponse(status=400)

    # create
    # - - - -
    try:
        user = User.objects.create_user(username, email, password)
        login(request, user)
        return HttpResponse(status=201)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
