
from django.http import HttpResponse

from proj.apps.chess.models import Chess


def get_view(request, uuid):
    return Chess.objects.get(uuid=uuid).__dict__
