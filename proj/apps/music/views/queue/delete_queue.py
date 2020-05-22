from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView

channel_layer = get_channel_layer()


@method_decorator(login_required, name="dispatch")
class DeleteQueueView(BaseView):
    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Queue = apps.get_model("music.Queue")
        Ticket = apps.get_model("music.Ticket")

        queue_uuid = request.POST.get("queue_uuid", None)

        queue = Queue.objects.select_related("stream").get(uuid=queue_uuid)
        queue.delete()

        queue_qs = (
            Queue.objects.select_related("stream", "record")
            .in_stream(queue.stream)
            .filter(created_at__gt=queue.created_at)
            .order_by("created_at")
        )

        payload = {
            "type": "send_update",
            "text": {
                "deleted": {"queues": [Queue.objects.serialize(queue)],},
                "updated": {
                    "queues": [Queue.objects.serialize(queue1) for queue1 in queue_qs]
                },
            },
        }

        queue.stream
        for ticket in Ticket.objects.administrators(stream=queue.stream):
            user_id = ticket.holder_id
            async_to_sync(channel_layer.group_send)(f"user-{user_id}", payload)

        return self.http_response_200({})
