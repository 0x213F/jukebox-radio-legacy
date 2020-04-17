from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def signin_view(request):

    # authenticate
    # - - - - - - -
    if request.user.is_authenticated:
        return HttpResponse(status=403)

    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user = authenticate(request, username=username, password=password)

    if user is None:
        return HttpResponse(status=400)

    # login the user
    # - - - - - - - -
    login(request, user)
    return HttpResponse(status=200)
