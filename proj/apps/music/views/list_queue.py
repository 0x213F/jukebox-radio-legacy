from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class ListQueueView(BaseView):
    def get(self, request, **kwargs):
        '''
        List all of the stream objects that a user can access.
        '''
        Queue = apps.get_model('music', 'Queue')
        Stream = apps.get_model('music', 'Stream')

        stream_uuid = request.GET.get('stream_uuid', None)
        stream = Stream.objects.get(uuid=stream_uuid)

        queue_qs = (
            Queue.objects
            .select_related('record')
            .filter(stream=stream, played_at__isnull=True)
            .order_by('created_at')
        )

        response = {
            'queue': Queue.objects.serialize_list(stream, queue_qs),
        }

        return self.http_response(response)
