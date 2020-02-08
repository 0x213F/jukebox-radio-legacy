from django.template.response import TemplateResponse

from proj.core.views import BaseView


class CreateStreamView(BaseView):
    def get(self, request, **kwargs):
        return TemplateResponse(request, "createstream.html")
