from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.apps.music.models import Queue


@method_decorator(login_required, name="dispatch")
class ListQueueView(BaseView):
    def get(self, request, **kwargs):
        """
        List all of the stream objects that a user can access.
        """

        stream_uuid = request.GET.get("stream_uuid", None)
        queue = Queue.objects.filter(stream__uuid=stream_uuid).order_by("created_at")

        print(Queue.objects.count())
        print(queue.count(), stream_uuid)

        response = {
            "queue": [Queue.objects.serialize(q) for q in queue],
        }
        return self.http_response(response)
