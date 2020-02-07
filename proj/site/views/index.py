from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


def index_view(request):
    if request.user.is_authenticated:
        if not request.user.profile.spotify_refresh_token:
            return HttpResponseRedirect("/linkspotify")
        return TemplateResponse(request, "home.html")

    return TemplateResponse(request, "index.html")
