from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView
from proj.apps.music.models import Comment
from proj.apps.music.models import Record
from proj.apps.music.models import Stream
from proj.apps.users.models import Profile


@method_decorator(login_required, name="dispatch")
class ListRecordsView(BaseView):
    def get(self, request, **kwargs):
        """
        List all of the stream objects that a user can access.
        """

        search_query = request.GET.get("query", None)

        records = Record.objects.filter(name__icontains=search_query).exclude(name__icontains='#hide').order_by("name")

        response = {
            "records": [Record.objects.serialize(s) for s in records],
        }
        return self.http_response(response)
