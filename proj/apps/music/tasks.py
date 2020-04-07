import json
from celery import shared_task
from datetime import datetime
from datetime import timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.apps import apps


channel_layer = get_channel_layer()



@shared_task
def schedule_spin(stream_id):
    Queue = apps.get_model('music', 'Queue')
    Record = apps.get_model("music.Record")
    Stream = apps.get_model("music.Stream")

    stream = Stream.objects.get(id=stream_id)

    if stream.paused_at:
        return

    now = datetime.now()
    if now < stream.tracklisting_terminates_at.replace(tzinfo=None):
        return

    queue = (
        Queue
        .objects
        .select_related('stream', 'record')
        .filter(stream=stream, played_at__isnull=True)
        .order_by("created_at")
        .first()
    )

    if not queue:
        stream.current_record = None
        stream.current_tracklisting = None
        stream.save()
        async_to_sync(channel_layer.group_send)(
            stream.chat_room,
            {
                "type": "sync_playback",
            },
        )
        return

    Stream.objects.spin(queue, stream)
