
import chess

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame


@login_required
def get_view(request):
    '''
    TODO docstring
    '''
    import chess

    code = request.GET.get('code', None)

    games = ChessGame.objects.active()
    if code:
        games = games.filter(code=code)
    else:
        games = games.belongs_to(request.user)

    if games.count() == 0:
        return HttpResponseNotFound()
    if games.count() != 1:
        RuntimeError('Multiple games found.')

    game = games.first()
    player = 'white 'if request.user == game.white else 'black'
    return JsonResponse({
        'board': game.board,
        'player': player,
    })
