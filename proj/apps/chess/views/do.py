
import chess

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import F
from django.http import HttpResponse
from django.http import JsonResponse


@login_required
def do_view(request):
    '''
    TODO docstring
    '''

    game = ChessGame.objects.active().belong_to(request.user).assert_singular()

    action_str = request.POST.get('action', None)
    if action not in ChessSnapshot.ACTION_CHOICES:
        return HttpResponse(status=500)

    action = getattr(ChessGame.objects, action_str)
    response = action(game, request.user)

    return JsonResponse(serialize(response))
