from datetime import datetime
from datetime import timedelta

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class ListStreamsView(BaseView):

    def get(self, request, **kwargs):
        '''
        List all of the stream objects that a user can access.
        '''
        Stream = apps.get_model('music', 'Stream')
        Ticket = apps.get_model('music', 'Ticket')
        Profile = apps.get_model('users', 'Profile')

        streams = Stream.objects.list_tune_in_streams(request.user).order_by('id')

        active_ticket = None
        active_stream_uuid = request.user.profile.active_stream_uuid
        if active_stream_uuid:
            active_ticket = Ticket.objects.get(
                holder=request.user, stream__uuid=active_stream_uuid,
            )

        now = datetime.now()

        response = {
            'streams': [
                Stream.objects.serialize(
                    s,
                    active_users=(
                        s.comments
                        .filter(
                            created_at__gte=now - timedelta(minutes=10),
                        )
                        .distinct('commenter_id')
                        .order_by('created_at')
                    )
                )
                for s in streams
            ],
            'user': (
                Profile.objects.serialize_user(
                    request.user, active_ticket=active_ticket
                )
            ),
        }
        return self.http_response(response)
