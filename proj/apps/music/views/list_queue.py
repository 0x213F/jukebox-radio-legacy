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

        stream_uuid = request.GET.get('stream_uuid', None)
        queue = (
            Queue.objects
            .filter(stream__uuid=stream_uuid, played_at__isnull=True)
            .order_by('created_at')
        )

        response = {
            'queue': [Queue.objects.serialize(q) for q in queue],
        }
        return self.http_response(response)
