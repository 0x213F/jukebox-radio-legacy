from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from random_username.generate import generate_username

from proj.core.views import BaseView

channel_layer = get_channel_layer()


@method_decorator(login_required, name="dispatch")
class CreateStreamView(BaseView):
    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Stream = apps.get_model("music.Stream")
        Ticket = apps.get_model("music.Ticket")

        if not request.user.profile.activated_at:
            self.http_response_403("Not permitted")

        stream_name = request.POST.get("name", None)
        tags = request.POST.get("tags", None)
        if not stream_name or not tags:
            self.http_response_400("Missing data")

        now = datetime.now()
        holder_name = (
            request.user.profile.default_display_name or generate_username(1)[0]
        )

        stream = Stream.objects.create(
            title=stream_name,
            tags=tags,
            owner=request.user,
            owner_name=holder_name,
            status=Stream.STATUS_ACTIVATED,
        )
        stream.unique_custom_id = str(stream.uuid)
        stream.save()

        Ticket.objects.create(
            stream=stream,
            holder=request.user,
            email=request.user.email,
            name=holder_name,
            is_administrator=True,
            updated_at=now,
        )

        async_to_sync(channel_layer.group_send)(
            "homepage",
            {
                "type": "send_update",
                "text": {"created": {"stream": [Stream.objects.serialize(stream)],}},
            },
        )

        return self.http_response_200({})
