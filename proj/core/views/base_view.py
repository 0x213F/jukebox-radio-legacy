
import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.views import View


class BaseView(View):
    '''
    TODO docstring
    '''

    def http_response(self, response):
        if type(response) == dict:
            print('~~~~~~~~~~~~~~~~~~~~~~~~')
            return JsonResponse(response)
        if type(response) == list:
            return JsonResponse(serialize('json', response), safe=False)
        return JsonResponse(serialize('json', [response])[1:-1], safe=False)
