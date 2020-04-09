from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.views import View


class BaseView(View):
    '''
    Inherits from Django View.
    '''

    def http_response_200(self, response):
        if type(response) == dict:
            return JsonResponse(response)
        if type(response) == list:
            return JsonResponse(serialize('json', response), safe=False)
        return JsonResponse(serialize('json', [response])[1:-1], safe=False)

    def http_response_400(self, message):
        return HttpResponseBadRequest(message)

    def http_response_403(self, message):
        return HttpResponseForbidden(message)

    def template_response(self, request, template, context={}):
        return TemplateResponse(request, template, context)

    def redirect_response(self, redirect_path):
        return HttpResponseRedirect(redirect_path)
