from django.template.response import TemplateResponse

from proj.core.views import BaseView


class RecordsListView(BaseView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")

        stream_uuid = request.GET.get("stream_uuid", None)

        return TemplateResponse(request, "recordslist.html", {'stream_uuid': stream_uuid})
