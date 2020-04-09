from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


@method_decorator(login_required, name='dispatch')
class DeleteQueueView(BaseView):
    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Queue = apps.get_model('music.Queue')
        Ticket = apps.get_model('music.Ticket')

        queue_id = request.POST.get('queue_id', None)

        queue = Queue.objects.select_related('stream').get(id=queue_id)
        queue.delete()

        tickets = Ticket.objects.filter(stream=queue.stream, is_administrator=True)
        for ticket in tickets:
            user_id = ticket.holder_id
            async_to_sync(channel_layer.group_send)(
                f'user-{user_id}', {'type': 'update_queue',},
            )

        return self.http_response_200({})
