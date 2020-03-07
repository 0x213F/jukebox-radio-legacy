from proj.core.views import BaseView


class AccountView(BaseView):
    def get(self, request, **kwargs):
        return self.template_response(request, 'account.html', {'default_display_name': request.user.profile.default_display_name or '', 'user': request.user})
