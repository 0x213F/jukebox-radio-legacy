from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from proj.apps.users.models import Profile


@csrf_protect
def create_view(request):

    # form validation
    # - - - - - - - -
    email = request.POST.get("email", None)
    password = request.POST.get("password", None)
    if not email or not password:
        return HttpResponse(status=400)

    # authentication
    # - - - - - - - -
    if request.user.is_authenticated:
        if request.user.profile.activated_at:
            raise ValueError('cannot change login of active user')
        request.user.email = email
        request.user.username = email
        request.user.set_password(password)
        request.user.save()
        return HttpResponse(status=201)

    # create
    # - - - -
    try:
        user = User.objects.create_user(email, email, password)
        Profile.objects.create(user=user, activated_at=datetime.now())
        login(request, user)
        return HttpResponse(status=201)
    except Exception as e:
        return HttpResponse(status=400)
