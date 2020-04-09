from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class DeleteStreamView(BaseView):
    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Stream = apps.get_model('music.Stream')

        stream_uuid = request.POST.get('stream_uuid', None)

        stream = Stream.objects.get(uuid=stream_uuid)

        if stream.owner != request.user:
            self.http_response_403('Not permitted')

        stream.delete()

        return self.http_response_200({})
