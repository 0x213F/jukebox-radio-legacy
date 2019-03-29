
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame


@login_required
def create_view(request):
    '''
    TODO docstring
    '''
    import chess
    import json
    import random

    pending_game = ChessGame.objects.active().belong_to(request.user)
    if pending_game.exists():
        return HttpResponse(status=500)

    player, opponent = random.shuffle(['black', 'white'])

    fields = {
        'board': chess.Board().fen(),
        'is_private': True,
        player: request.user,
        f'{player}_status': ChessGame.STATUS_PENDING_GAME_START,
        f'{opponent}_status': ChessGame.STATUS_PENDING_OPPONENT,
    }

    new_game = ChessGame.objects.create(**fields)

    return JsonResponse(serialize(new_game))
