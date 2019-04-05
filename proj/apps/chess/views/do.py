
import chess

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import F
from django.http import HttpResponse
from django.http import JsonResponse


@login_required
def do_view(request):
    '''
    Generic POST endpoint to perform methods related to `ChessGame`.
    '''

    action = request.POST.get('thing', None)
    if action not in ChessSnapshot.ACTION_CHOICES:
        return HttpResponse(status=500)

    result = Chess.objects.do(action, request)
    response = Chess.objects.response(result)

    return JsonResponse(serialize(response))
