
import chess

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class JoinMatchView(BaseView):
    '''
    TODO docstring
    '''

    def post(self, request, **kwargs):
        '''
        TODO docstring
        '''

        try:
            game = ChessGame.objects.active().belongs_to(request.user).get()
            raise Exception('User is already active in a private game.')
        except ChessGame.DoesNotExist:
            pass

        join_code = request.POST.get('join_code', None)
        result = ChessGame.objects.join_match(request.user, join_code)

        response = ChessGame.objects.response(result, request)
        return self.http_response(response)
