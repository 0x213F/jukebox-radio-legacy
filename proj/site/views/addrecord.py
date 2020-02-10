from django.template.response import TemplateResponse

from proj.core.views import BaseView


class AddRecordView(BaseView):
    def get(self, request, **kwargs):
        return TemplateResponse(request, "addrecord.html")
