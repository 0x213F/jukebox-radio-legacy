
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from proj.apps.users.models import Profile


@csrf_protect
def create_view(request):

    # authentication
    # - - - - - - - -
    if request.user.is_authenticated:
        return HttpResponse(status=403)


    # form validation
    # - - - - - - - -
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if not email or not password:
        return HttpResponse(status=400)

    # create
    # - - - -
    try:
        user = User.objects.create_user(email, email, password)
        Profile.objects.create(user=user)
        login(request, user)
        return HttpResponse(status=201)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
