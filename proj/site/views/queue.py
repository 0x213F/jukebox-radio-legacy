from django.apps import apps
from django.template.response import TemplateResponse

from proj.core.views import BaseView


class QueueView(BaseView):
    def get(self, request, stream, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")

        Stream = apps.get_model('music', 'Stream')
        stream = Stream.objects.get(uuid=stream)
        return TemplateResponse(request, "queue.html", {'stream': stream})
