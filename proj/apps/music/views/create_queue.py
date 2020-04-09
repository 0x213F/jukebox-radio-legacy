from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView


channel_layer = get_channel_layer()


@method_decorator(login_required, name='dispatch')
class CreateQueueView(BaseView):
    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Queue = apps.get_model('music.Queue')
        Record = apps.get_model('music.Record')
        Stream = apps.get_model('music.Stream')
        Ticket = apps.get_model('music.Ticket')

        spotify_uri = request.POST.get('uri', None)
        img = request.POST.get('img', None)
        record_name = request.POST.get('record_name', None)

        stream_uuid = request.POST.get('stream_uuid', None)

        record = Record.objects.get_or_create_from_uri(
            spotify_uri, record_name=record_name, img=img, user=request.user,
        )
        stream = Stream.objects.get(uuid=stream_uuid)

        queue = Queue.objects.create(record=record, stream=stream, user=request.user,)

        now = datetime.now()

        try:
            should_play_song = now > stream.record_terminates_at.replace(tzinfo=None)
        except Exception:
            should_play_song = True

        if should_play_song:
            stream, queue = Stream.objects.spin(queue, stream)
        else:
            tickets = Ticket.objects.filter(stream=stream, is_administrator=True)
            for ticket in tickets:
                user_id = ticket.holder_id
                async_to_sync(channel_layer.group_send)(
                    f'user-{user_id}', {'type': 'update_queue',},
                )

        return self.http_response_200({})
