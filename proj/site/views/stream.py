from django.template.response import TemplateResponse

from proj.core.views import BaseView


class StreamView(BaseView):
    def get(self, request, stream, **kwargs):
        print(stream)
        return TemplateResponse(request, "stream.html")
