from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def signout_view(request):

    # If you press logout you get forgotten.
    #   -- Saba
    logout(request)
    return HttpResponse(status=200)
