from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView


@method_decorator(login_required, name='dispatch')
class UpdateStreamView(BaseView):

    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Stream = apps.get_model('music.Stream')

        stream_uuid = request.POST.get('stream_uuid', None)
        stream_name = request.POST.get('stream_name', None)
        stream_tags = request.POST.get('stream_tags', None)
        unique_custom_id = request.POST.get('unique_custom_id', None)

        if len(stream_tags) > 3:
            raise ValueError('Too many emojis')

        stream_tags = ', '.join([char for char in stream_tags])

        if not stream_name or not stream_tags:
            raise Exception('Missing required parameters')

        kwargs = {}
        if unique_custom_id:
            kwargs['unique_custom_id'] = unique_custom_id

        Stream.objects.filter(uuid=stream_uuid).update(title=stream_name, tags=stream_tags, **kwargs)

        return self.http_response({})
