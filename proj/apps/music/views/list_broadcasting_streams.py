from datetime import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.apps.music.models import Comment
from proj.apps.music.models import Ticket
from proj.apps.music.models import Stream
from proj.apps.users.models import Profile


@method_decorator(login_required, name="dispatch")
class ListBroadcastingStreamsView(BaseView):
    def get(self, request, **kwargs):
        """
        List all of the stream objects that a user can access.
        """
        streams = Stream.objects.list_broadcasting_streams(request.user).order_by("id")

        now = datetime.now()

        response = {
            "streams": [
                Stream.objects.serialize(
                    s,
                    active_users=(
                        s.comments
                        .filter(
                            created_at__gte=now - timedelta(minutes=10),
                            commenter_id__isnull=False,
                        )
                        .distinct('commenter_id')
                        .order_by('commenter_id')
                    )
                )
                for s in streams
            ],
            "user": (
                Profile.objects.serialize_user(
                    request.user,
                )
            ),
        }
        return self.http_response(response)
