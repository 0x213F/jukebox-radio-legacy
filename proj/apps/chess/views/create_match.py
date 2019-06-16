
import chess

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class CreateMatchView(BaseView):
    '''
    TODO docstring
    '''

    def post(self, request, **kwargs):
        '''
        TODO docstring
        '''

        try:
            game = ChessGame.objects.get_private_game(request.user)
            raise Exception('User is already active in a private game.')
        except ChessGame.DoesNotExist:
            pass

        result = ChessGame.objects.create_match(request.user)

        response = ChessGame.objects.response(result, request)
        return self.http_response(response)
