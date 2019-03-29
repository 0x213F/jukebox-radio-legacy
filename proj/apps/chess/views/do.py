
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

    action_str = request.POST.get('thing', None)
    if action not in ChessSnapshot.ACTION_CHOICES:
        return HttpResponse(status=500)

    do_thing = getattr(ChessGame.objects, action_str)
    with_action = request.POST.get('with_action', {})
    response = do_thing(request.user, **with_action)

    return JsonResponse(serialize(response))

    # todo turn this into a decorator
    # game = (
    #     ChessGame.objects.active().belong_to(request.user).assert_singular()
    #     or
    #     ChessGame.objects.active().public().assert_singular()
    # )
