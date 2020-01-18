from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps

from proj.core.views import BaseView


SUBSCRIBED = "subscribed"
UNSUBSCRIBED = "unsubscribed"


@method_decorator(login_required, name="dispatch")
class UpdateStreamView(BaseView):

    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Stream = apps.get_model("music.Stream")

        stream_uuid = request.POST.get("stream_uuid", None)
        stream_status = request.POST.get("stream_status", None)

        if not stream_uuid or not stream_status:
            raise Exception('Missing required parameters')

        Stream.objects.filter(uuid=stream_uuid).update(status=stream_status)

        return self.http_response({})
