import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from proj.core.views import BaseView

channel_layer = get_channel_layer()


@method_decorator(login_required, name="dispatch")
class UpdateTicketView(BaseView):
    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Ticket = apps.get_model("music.Ticket")
        Profile = apps.get_model("users.Profile")

        email = request.POST.get("email", None)
        holder_name = request.POST.get("display_name", None)
        is_administrator = request.POST.get("is_administrator", None)
        is_administrator = is_administrator == "true"
        stream_uuid = request.POST.get("stream_uuid", None)
        is_hidden_when_idle = request.POST.get("is_hidden_when_idle", None)
        is_hidden_when_idle = is_hidden_when_idle == "on"

        ticket = Ticket.objects.select_related("stream").get(
            email=request.user.email, stream__uuid=stream_uuid,
        )
        stream = ticket.stream

        if email:
            if not stream.owner == request.user:
                return self.http_response_403("Not permitted")
            if is_administrator:
                Ticket.objects.promote_to_host(email, stream)
            else:
                Ticket.objects.demote_from_host(email, stream)
        else:
            if holder_name:
                ticket.name = holder_name
            if is_hidden_when_idle:
                if stream.owner == request.user:
                    return self.http_response_403("Not permitted")
                ticket.is_hidden_when_idle = is_hidden_when_idle

            if holder_name or is_hidden_when_idle:
                ticket.save()
                user = ticket.holder
                async_to_sync(channel_layer.group_send)(
                    f"user-{user.id}",
                    {
                        "type": "send_update",
                        "text": {
                            "updated": {
                                "users": [
                                    Profile.objects.serialize_user(
                                        user, active_ticket=ticket
                                    )
                                ],
                            }
                        },
                    },
                )
            if stream.owner_id == request.user.id:
                stream.owner_name = holder_name
                stream.save()

        return self.http_response_200({})
