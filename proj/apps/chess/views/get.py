
import chess

from django.http import JsonResponse

from proj.apps.chess.models import Chess

def get_view(request):

    import chess
    uuid = request.GET.get('uuid', None)
    game = Chess.objects.get(uuid=uuid)

    if request.user == game.white:
        return JsonResponse({
            'board': game.board,
            'player': 'white',
        })
    else:
        return JsonResponse({
            'board': game.board,
            'player': 'black',
        })
