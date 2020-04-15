from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        stream_is_private = request.POST.get('stream_is_private', None)
        unique_custom_id = request.POST.get('unique_custom_id', None)

        is_private = stream_is_private == 'on'

        if not stream_name or not stream_tags:
            self.http_response_400('Missing data')

        kwargs = {}
        if unique_custom_id:
            kwargs['unique_custom_id'] = unique_custom_id

        Stream.objects.filter(uuid=stream_uuid).update(
            title=stream_name, tags=stream_tags, is_private=is_private, **kwargs
        )

        return self.http_response_200({'unique_custom_id': unique_custom_id})
