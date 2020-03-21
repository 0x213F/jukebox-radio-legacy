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

    queue = (
        Queue
        .objects
        .select_related('stream', 'record')
        .filter(stream=stream, played_at__isnull=True)
        .order_by("created_at")
        .first()
    )
    if not queue:
        async_to_sync(channel_layer.group_send)(
            stream.chat_room,
            {
                "type": "send_waiting_status",
                "text": json.dumps(
                    {
                        "source": {
                            "type": "system",
                            "display_name": None,
                            "uuid": None,
                        },
                        "data": {
                            "stream": Stream.objects.serialize(stream),
                            "playback": {
                                "status": 'waiting-for-stream-to-start',
                            },
                        },
                    }
                ),
            },
        )
        return

    record = queue.record

    Stream.objects.spin(record, stream)

    now = datetime.now()
    queue.played_at = now
    queue.save()

    next_play = now + timedelta(milliseconds=(record.duration_ms))  # + 250

    schedule_spin.apply_async(eta=next_play, args=[stream_id])
