
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


def route_view(request, route, uuid=None):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, f'{route}.html')
