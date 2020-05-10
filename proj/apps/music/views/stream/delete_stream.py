from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView


channel_layer = get_channel_layer()


@method_decorator(login_required, name='dispatch')
class DeleteStreamView(BaseView):
    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Stream = apps.get_model('music.Stream')
        Ticket = apps.get_model('music', 'Ticket')

        stream_uuid = request.POST.get('stream_uuid', None)

        stream = Stream.objects.get(uuid=stream_uuid)

        if stream.owner != request.user:
            self.http_response_403('Not permitted')

        stream.unique_custom_id = str(stream.uuid)
        stream.save()

        stream.delete()

        for ticket in Ticket.objects.filter(is_active=True, stream=stream):
            user_id = ticket.holder_id
            async_to_sync(channel_layer.group_send)(
                f'user-{user_id}',
                {
                    'type': 'send_update',
                    'text': {
                        'deleted': {
                            'stream': [Stream.objects.serialize(stream)],
                        }
                    }
                },
            )

        async_to_sync(channel_layer.group_send)(
            'homepage',
            {
                'type': 'send_update',
                'text': {
                    'deleted': {
                        'stream': [Stream.objects.serialize(stream)],
                    }
                }
            },
        )

        return self.http_response_200({})
