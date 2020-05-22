from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView

channel_layer = get_channel_layer()


@method_decorator(login_required, name="dispatch")
class UpdateStreamView(BaseView):
    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Stream = apps.get_model("music.Stream")

        stream_uuid = request.POST.get("stream_uuid", None)
        stream_name = request.POST.get("stream_name", None)
        stream_tags = request.POST.get("stream_tags", None)
        stream_is_private = request.POST.get("stream_is_private", None)
        unique_custom_id = request.POST.get("unique_custom_id", None)

        is_private = stream_is_private == "on"

        stream = Stream.objects.get(uuid=stream_uuid)

        if not stream.owner == request.user:
            return self.http_response_403("Must be stream owner")

        if not stream_name or not stream_tags:
            return self.http_response_400("Missing data")

        if not unique_custom_id.isalnum() and "-" not in unique_custom_id:
            return self.http_response_400("Invalid character")

        stream.title = stream_name
        stream.tags = stream_tags
        stream.is_private = is_private
        if unique_custom_id:
            stream.unique_custom_id = unique_custom_id

        stream.save()

        async_to_sync(channel_layer.group_send)(
            stream.chat_room,
            {
                "type": "send_update",
                "text": {"updated": {"streams": [Stream.objects.serialize(stream)],}},
            },
        )

        return self.http_response_200({"unique_custom_id": unique_custom_id})
