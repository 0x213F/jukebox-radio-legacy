
from django.http import HttpResponse


def get_view(request):
    return HttpResponse(status=405)
