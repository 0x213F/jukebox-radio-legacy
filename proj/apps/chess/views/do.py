
import chess

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import F
from django.http import JsonResponse


def do_view(request):
    '''
    Generic POST endpoint to perform methods related to `ChessGame`.
    '''
    from proj.apps.chess.models import ChessSnapshot
    from proj.apps.chess.models import ChessGame

    action_slug = request.POST.get('thing')
    action_method = action_slug.replace('-', '_')
    if action_method not in [c[0] for c in ChessSnapshot.ACTION_CHOICES]:
        return HttpResponse(status=500)

    result = ChessGame.objects.do(action_method, request)
    response = ChessGame.objects.response(result, request)

    return JsonResponse(response, safe=False)
