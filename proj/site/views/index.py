from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


def index_view(request):
    if request.user.is_authenticated:
        return TemplateResponse(request, "home.html")

    return TemplateResponse(request, "index.html")
