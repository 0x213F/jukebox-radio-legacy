
import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.views import View


class BaseView(View):
    '''
    TODO docstring
    '''

    def _http_response_object(self, obj):
        return JsonResponse(serialize('json', [obj])[1:-1], safe=False)
