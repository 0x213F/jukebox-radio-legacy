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
        Profile = apps.get_model('users', 'Profile')

        stream_type = request.GET.get('stream_type', None)

        if stream_type == 'broadcasting':
            streams = Stream.objects.list_broadcasting_streams(request.user).order_by('id')
        else:
            streams = Stream.objects.list_tune_in_streams(request.user).order_by('id')

        response = {
            'streams': [
                Stream.objects.serialize(
                    s, active_users=s.tickets.filter(is_active=True)
                )
                for s in streams
            ],
            'user': (Profile.objects.serialize_user(request.user,)),
        }
        return self.http_response_200(response)
