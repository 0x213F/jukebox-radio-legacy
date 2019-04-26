
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from proj.apps.users.forms import UserForm

User = get_user_model()


@csrf_protect
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
        print('what')
        return HttpResponse(status=400)

    # # recovery options
    # # - - - - - - - - -
    # email_addr = request.POST.get('email', None)
    # phone_num = request.POST.get('phone', None)
    # if (not email_addr) and (not phone_num):
    #     return HttpResponse(status=400)
    #
    # # verify
    # # - - - - - -
    # Email.verify(email_addr) if email_addr else SMS.verify(phone_num)

    # create
    # - - - -
    try:
        user = User.objects.create(username, password)
        login(request, user)
        return HttpResponse(status=201)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
