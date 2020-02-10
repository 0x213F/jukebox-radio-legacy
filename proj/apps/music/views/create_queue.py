import uuid
from datetime import datetime
from datetime import timedelta

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView
from proj.apps.music import tasks


@method_decorator(login_required, name="dispatch")
class CreateQueueView(BaseView):

    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Queue = apps.get_model("music.Queue")
        Record = apps.get_model("music.Record")
        Stream = apps.get_model("music.Stream")

        record_id = request.POST.get("record_id", None)
        stream_uuid = request.POST.get("stream_uuid", None)

        record = Record.objects.get(id=record_id)
        stream = Stream.objects.get(uuid=stream_uuid)

        queue = Queue.objects.create(
            record=record,
            stream=stream,
            user=request.user,
        )

        now = datetime.now()

        try:
            should_play_song = (
                now > stream.record_terminates_at.replace(tzinfo=None)
            )
        except Exception:
            should_play_song = True

        if should_play_song:
            stream.last_status_change_at = now
            stream.status = Stream.STATUS_ACTIVATED
            stream.save()
            Stream.objects.spin(record, stream)
            queue.played_at = now
            queue.save()
            next_play_time = (
                stream.record_terminates_at.replace(tzinfo=None) +
                timedelta(milliseconds=250)
            )
            tasks.schedule_spin.apply_async(eta=next_play_time, args=[stream.id])

        return self.http_response({})
