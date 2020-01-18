from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView
from proj.apps.music.models import Comment
from proj.apps.music.models import Ticket
from proj.apps.music.models import Stream
from proj.apps.users.models import Profile


SUBSCRIBED = "subscribed"
UNSUBSCRIBED = "unsubscribed"


@method_decorator(login_required, name="dispatch")
class SpinRecordView(BaseView):
    def put(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Record = apps.get_model("music.Record")
        Stream = apps.get_model("music.Stream")

        record_id = request.POST.get("record_id", None)
        stream_uuid = request.POST.get("stream_uuid", None)

        now = datetime.now()
        try:
            pre_save_stream = Stream.objects.get(uuid=stream_uuid)
            if pre_save_stream.current_record and pre_save_stream.record_terminates_at:
                if now < pre_save_stream.record_terminates_at.replace(tzinfo=None):
                    raise Exception(
                        'The record cannot be changed since one is still '
                        'playing.'
                    )
        except Stream.DoesNotExist:
            raise Exception('Stream does not exist')

        next_record = Record.objects.get(id=record_id)
        pre_save_stream.record = next_record
        pre_save_stream.save()

        if not next_record:
            return

        Stream.objects.spin(next_record, stream)

        return self.http_response({})
