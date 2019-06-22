
import chess

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class UndoResponseView(BaseView):
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

        if not game.is_users_turn(request.user):
            raise Exception('It is the opponent\'s turn')

        response = request.POST.get('response', None)
        if reponse == 'approve':
            result = ChessGame.objects.approve_undo(game, request.user)
        elif response == 'reject':
            result = ChessGame.objects.reject_undo(game, request.user)
        else:
            raise Exception('Invalid undo response.')

        response = ChessGame.objects.response(result, request)
        return self.http_response(response)
