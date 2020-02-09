from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.apps.music.models import Comment
from proj.apps.music.models import Ticket
from proj.apps.music.models import Stream
from proj.apps.users.models import Profile


@method_decorator(login_required, name="dispatch")
class ListStreamsView(BaseView):
    def get(self, request, **kwargs):
        """
        List all of the stream objects that a user can access.
        """
        broadcasting_ids = Stream.objects.list_broadcasting_streams(request.user).order_by("id").values_list('id', flat=True)

        streams = Stream.objects.list_streams(request.user).order_by("id")

        active_ticket = None
        active_stream_uuid = request.user.profile.active_stream_uuid
        if active_stream_uuid:
            active_ticket = Ticket.objects.get(
                holder=request.user, stream__uuid=active_stream_uuid,
            )

        streams_data = []
        for s in streams:
            if s.id in broadcasting_ids:
                continue
            streams_data.append(Stream.objects.serialize(s))

        response = {
            "streams": streams_data,
            "user": (
                Profile.objects.serialize_user(
                    request.user, active_ticket=active_ticket
                )
            ),
        }
        return self.http_response(response)
