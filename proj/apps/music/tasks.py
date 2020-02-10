from celery import shared_task
from datetime import datetime
from datetime import timedelta

from django.apps import apps


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
        return

    record = queue.record

    Stream.objects.spin(record, stream)
    queue.delete()

    now = datetime.now()
    next_play = now + timedelta(milliseconds=(record.duration_ms + 250))

    schedule_spin.apply_async(eta=next_play, args=[stream_id])
