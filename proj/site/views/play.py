
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


def play_view(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, 'play.html')
