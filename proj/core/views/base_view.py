import json

from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views import View


class BaseView(View):
    """
    TODO docstring
    """

    def http_response(self, response):
        if type(response) == dict:
            return JsonResponse(response)
        if type(response) == list:
            return JsonResponse(serialize("json", response), safe=False)
        return JsonResponse(serialize("json", [response])[1:-1], safe=False)

    def template_response(self, request, template, context={}):
        return TemplateResponse(request, template, context)

    def redirect_response(self, redirect_path):
        return HttpResponseRedirect(redirect_path)
