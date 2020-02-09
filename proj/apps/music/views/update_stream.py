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
        stream_name = request.POST.get("stream_name", None)
        stream_tags = request.POST.get("stream_tags", None)

        if not stream_name or not stream_tags:
            raise Exception('Missing required parameters')

        Stream.objects.filter(uuid=stream_uuid).update(title=stream_name, tags=stream_tags)

        return self.http_response({})
