
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse


def logout_view(request):

    # If you press logout you get forgotten.
    #   -- Saba
    logout(request)
    return HttpResponse(status=200)
