
import chess

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import F
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class SuggestMoveView(BaseView):
    '''
    TODO docstring
    '''

    def post(self, request, **kwargs):
        '''
        TODO docstring
        '''
        from proj.apps.chess.models import ChessSnapshot
        from proj.apps.chess.models import ChessGame

        action_slug = request.POST.get('thing')
        action_method = action_slug.replace('-', '_')
        if action_method not in [c[0] for c in ChessSnapshot.ACTION_CHOICES]:
            return HttpResponse(status=500)

        result = ChessGame.objects.suggest_move(action_method, request)

        response = ChessGame.objects.response(result, request)
        return self.http_response(response)
