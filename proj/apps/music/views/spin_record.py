from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime

from django.apps import apps

from proj.core.views import BaseView


SUBSCRIBED = "subscribed"
UNSUBSCRIBED = "unsubscribed"


@method_decorator(login_required, name="dispatch")
class SpinRecordView(BaseView):
    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Record = apps.get_model("music.Record")
        Stream = apps.get_model("music.Stream")

        record_id = request.POST.get("record_id", None)
        stream_uuid = request.POST.get("stream_uuid", None)

        now = datetime.now()
        stream = Stream.objects.get(uuid=stream_uuid)

        if stream.status != Stream.STATUS_ACTIVATED:
            raise Exception('The stream is not active')

        record_on_table = stream.current_record and stream.record_terminates_at
        if record_on_table:
            record_is_playing = (
                now < stream.record_terminates_at.replace(tzinfo=None)
            )
            if record_is_playing:
                raise Exception(
                    'The record cannot be changed since one is still '
                    'playing.'
                )

        next_record = Record.objects.get(id=record_id)
        stream.record = next_record
        stream.save()

        if not next_record:
            return

        Stream.objects.spin(next_record, stream)

        return self.http_response({})
