
import chess

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class UndoRequestView(BaseView):
    '''
    TODO docstring
    '''

    def post(self, request, **kwargs):
        '''
        TODO docstring
        '''

        game = ChessGame.objects.active().belongs_to(request.user).get()

        if game.is_started:
            raise Exception('There are no moves to undo.')

        if game.is_users_turn(request.user):
            raise Exception('It is the user\'s turn')

        result = ChessGame.objects.ask_undo(game, request.user)

        response = ChessGame.objects.response(result, request)
        return self.http_response(response)
