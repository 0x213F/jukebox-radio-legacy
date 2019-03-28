

from django.contrib.auth.decorators import login_required
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

    fields = {'board': chess.Board().fen()}
    player = random.choice(['black', 'white'])
    fields[player] = request.user

    chess = ChessGame.objects.create(**fields)

    return JsonResponse({
        'code': chess.code,
        'player': player,
    })
