
import chess

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from proj.apps.chess.models import ChessGame

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class GetView(BaseView):
    '''
    TODO docstring
    '''

    def get(self, request):
        '''
        TODO docstring
        '''

        uuid = request.GET.get('uuid', None)
        if uuid:
            game = ChessGame.objects.get(uuid=uuid)

        else:
            game = (
                ChessGame.objects.
                active().
                belong_to(request.user).
                get_singular()
            )

        return self._http_response_object(game)
