
import random
import string

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from proj.apps.users.forms import UserForm

User = get_user_model()


def index_view(request):

    # user must be logged out see homepage
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')

    return TemplateResponse(request, 'index.html')
