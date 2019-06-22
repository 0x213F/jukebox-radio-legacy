
import chess
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse

from proj.apps.chess.models import ChessGame
from proj.core.views import BaseView

@method_decorator(login_required, name='dispatch')
class ListMatchesView(BaseView):
    '''
    TODO docstring
    '''

    def post(self, request, **kwargs):
        '''
        TODO docstring
        '''
        return self.http_response(ChessGame.objects.belongs_to(request.user))
