
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth import authenticate


def authenticate_view(request):

    # authentication
    # - - - - - - - -
    if request.user.is_authenticated:
        return HttpResponse(status=403)

    # authenticate
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(request, username=username, password=password)

    if user is None:
        return HttpResponse(status=400)

    # login the user
    login(request, user)
    return HttpResponse(status=200)
