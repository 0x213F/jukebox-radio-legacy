
import chess

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class CloseMatchView(BaseView):
    '''
    TODO docstring
    '''

    def post(self, request, **kwargs):
        '''
        TODO docstring
        '''

        game = ChessGame.objects.get_private_game(request.user)

        if game.is_started:
            raise Exception('Cannot close a match that has already started.')

        result = ChessGame.objects.close_match(game, request.user)

        response = ChessGame.objects.response(result, request)
        return self.http_response(response)
