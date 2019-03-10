
from django.http import HttpResponse


def move_view(request):
    return HttpResponse(status=405)
