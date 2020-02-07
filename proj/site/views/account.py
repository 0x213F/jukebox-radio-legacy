from django.template.response import TemplateResponse

from proj.core.views import BaseView


class AccountView(BaseView):
    def get(self, request, **kwargs):
        return TemplateResponse(request, "account.html", {'default_display_name': request.user.profile.default_display_name or '', 'user': request.user})
