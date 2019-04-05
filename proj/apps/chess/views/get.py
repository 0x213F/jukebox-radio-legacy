
import chess

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame


@login_required
def list_view(request):
    '''
    TODO docstring
    '''

    game = ChessGame.objects.active().belong_to(request.user).get_singular()

    return JsonResponse(serialize(game))
