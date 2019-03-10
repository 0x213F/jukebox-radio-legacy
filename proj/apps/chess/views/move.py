
import chess

from django.http import HttpResponse


def move_view(request, uuid):
    game = Chess.objects.get(uuid=uuid)
    board = chess.Board(game.board)

    uci = request.POST.get('uci', None)
    try:
        move = chess.Move.from_uci(uci)
        board.push(move)
        updated_board = board.fen()
        game.update(board=updated_board)

        return updated_board.__dict__
    except Exception:
        return HttpResponse(status=500)
