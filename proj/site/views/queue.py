from django.apps import apps
from django.template.response import TemplateResponse

from proj.core.views import BaseView


class QueueView(BaseView):
    def get(self, request, stream, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")

        Ticket = apps.get_model('music', 'Ticket')
        Stream = apps.get_model('music', 'Stream')
        stream = Stream.objects.get(uuid=stream)

        Ticket.objects.get(holder=request.user, stream=stream, is_administrator=True)

        return TemplateResponse(request, "queue.html", {'stream': stream})
