

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from proj.apps.chess.models import Chess


@login_required
def create_view(request):

    import chess
    import json
    import random

    # create
    # - - - -
    fields = {
        'board': chess.Board().fen(),
    }
    player = random.choice(['black', 'white'])
    fields[player] = request.user
    chess = Chess.objects.create(**fields)
    return JsonResponse({
        'uuid': chess.uuid,
        'player': player,
    })
