from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from django.apps import apps


channel_layer = get_channel_layer()


@shared_task
def schedule_spin(stream_id):
    Queue = apps.get_model('music', 'Queue')
    Stream = apps.get_model('music.Stream')

    stream = Stream.objects.get(id=stream_id)

    queue = Queue.objects.select_related('stream', 'record').get_up_next(stream)

    Stream.objects.spin(queue, stream)
