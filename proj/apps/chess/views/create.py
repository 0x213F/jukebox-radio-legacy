
import json

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

    player = random.choice(list(ChessGame.PLAYER_CHOICES))

    fields = dict({
        'board': chess.Board().fen(),
        'is_private': True,
    })
    fields[f'{player}_user'] = request.user

    new_game = ChessGame.objects.create(**fields)

    return JsonResponse(json.dumps(serialize('json', [new_game])), safe=False)
