
import chess

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse


@login_required
def move_view(request):
    '''
    TODO docstring
    '''
    games = games.belongs_to(request.user)
    if games.count() == 0:
        return HttpResponseNotFound()
    if games.count() != 1:
        RuntimeError('Multiple games found.')

    game = games.first()
    board = chess.Board(game.board)
    uci = request.POST.get('uci', None)

    try:
        move = chess.Move.from_uci(uci)
        board.push(move)
        updated_board = board.fen()
        game.update(board=updated_board)
        return JsonResponse(updated_board.__dict__)

    except Exception:
        return HttpResponse(status=500)
