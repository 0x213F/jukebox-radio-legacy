from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from proj.core.views import BaseView


class LinkSpotifyView(BaseView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")

        return TemplateResponse(request, "linkspotify.html")
