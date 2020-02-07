from django.template.response import TemplateResponse

from proj.core.views import BaseView


class LinkSpotifyView(BaseView):
    def get(self, request, **kwargs):
        return TemplateResponse(request, "linkspotify.html")
