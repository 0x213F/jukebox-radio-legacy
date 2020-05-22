from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.apps.music.models import Ticket
from proj.apps.users.models import Profile
from proj.core.views import BaseView


@method_decorator(login_required, name="dispatch")
class ListTicketsView(BaseView):
    def get(self, request, **kwargs):
        """
        List all of the ticket objects which are hosts.
        """
        stream_uuid = request.GET.get("stream_uuid", None)

        tickets = Ticket.objects.filter(stream__uuid=stream_uuid, is_administrator=True)

        active_ticket = Ticket.objects.get(
            email=request.user.email, stream__uuid=stream_uuid,
        )

        tickets_data = []
        for t in tickets:
            if t.id == active_ticket.id:
                continue
            tickets_data.append(Ticket.objects.serialize(t))

        response = {
            "tickets": tickets_data,
            "user": (
                Profile.objects.serialize_user(
                    request.user, active_ticket=active_ticket
                )
            ),
        }
        return self.http_response_200(response)
