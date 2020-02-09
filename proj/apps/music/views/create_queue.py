from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


@method_decorator(login_required, name="dispatch")
class CreateQueueView(BaseView):

    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Queue = apps.get_model("music.Queue")
        Stream = apps.get_model("music.Stream")

        record_id = request.POST.get("record_id", None)
        stream_uuid = request.POST.get("stream_uuid", None)

        stream = Stream.objects.get(uuid=stream_uuid)

        print(stream_uuid)

        Queue.objects.create(
            record_id=record_id,
            stream=stream,
            user=request.user,
        )

        return self.http_response({})
