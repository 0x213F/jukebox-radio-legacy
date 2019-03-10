
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from proj.apps.chess.models import Chess


@login_required
def create_view(request):

    # create
    # - - - -
    fields = {
        board=chess.Board().fen(),
    }
    attr(fields, random.choice('black, white'), request.user)
    chess = Chess.objects.create(**fields)
    return HttpResponse(status=200)
