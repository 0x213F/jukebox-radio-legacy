from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


@method_decorator(login_required, name="dispatch")
class DeleteQueueView(BaseView):

    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Queue = apps.get_model("music.Queue")

        queue_id = request.POST.get("queue_id", None)

        queue = Queue.objects.get(id=queue_id)
        queue.delete()

        return self.http_response({})
