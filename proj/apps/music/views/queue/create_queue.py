import uuid
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView

channel_layer = get_channel_layer()


@method_decorator(login_required, name="dispatch")
class CreateQueueView(BaseView):
    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Queue = apps.get_model("music", "Queue")
        Stream = apps.get_model("music", "Stream")
        Ticket = apps.get_model("music", "Ticket")

        stream_uuid = request.POST.get("stream_uuid", None)
        provider = request.POST.get("provider", None)
        storage_type = request.POST.get("storage_type", None)

        stream = Stream.objects.get(uuid=stream_uuid)

        if provider == "spotify":
            record, queue = self.create_spotify_queue(request, stream)
        elif provider == "youtube":
            record, queue = self.create_youtube_queue(request, stream)
        elif provider == "storage":
            if storage_type == "file":
                if not request.user.is_staff:
                    raise ValueError("Needs to be staff")
            record, queue = self.create_file_queue(request, stream, storage_type)
        else:
            raise ValueError("Needs ID")

        now = datetime.now()
        if stream.record_terminates_at:
            should_play_song = now > stream.record_terminates_at.replace(tzinfo=None)
        else:
            should_play_song = True

        if should_play_song:
            stream, queue = Stream.objects.spin(queue, stream)
        else:
            payload = {
                "type": "send_update",
                "text": {"created": {"queues": [Queue.objects.serialize(queue)],}},
            }

            for ticket in Ticket.objects.administrators(stream=stream):
                user_id = ticket.holder_id
                async_to_sync(channel_layer.group_send)(f"user-{user_id}", payload)

        return self.http_response_200({})

    def create_spotify_queue(self, request, stream):
        QueueListing = apps.get_model("music", "QueueListing")
        Queue = apps.get_model("music.Queue")
        Record = apps.get_model("music.Record")
        Ticket = apps.get_model("music.Ticket")

        spotify_uri = request.POST.get("spotify_uri", None)
        img = request.POST.get("img", None)
        record_name = request.POST.get("record_name", None)

        record = Record.objects.get_or_create_from_uri(
            spotify_uri, record_name=record_name, img=img, user=request.user,
        )

        queue = Queue.objects.create(record=record, stream=stream, user=request.user)

        return record, queue

    def create_youtube_queue(self, request, stream):
        Queue = apps.get_model("music.Queue")
        Record = apps.get_model("music.Record")

        youtube_id = request.POST.get("youtube_id", None)

        record = Record.objects.get_or_create_from_youtube_id(youtube_id)

        queue = Queue.objects.create(record=record, stream=stream, user=request.user,)

        return record, queue

    def create_file_queue(self, request, stream, storage_type):
        Record = apps.get_model("music.Record")
        Queue = apps.get_model("music.Queue")

        file = request.FILES["file"]

        record = Record.objects.create_from_file(file, storage_type)

        queue = Queue.objects.create(record=record, stream=stream, user=request.user,)

        return record, queue
