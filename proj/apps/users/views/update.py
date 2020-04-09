from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from proj.core.views import BaseView


@method_decorator(login_required, name="dispatch")
class UpdateView(BaseView):
    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        display_name = request.POST.get("display_name", None)
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)

        request.user.profile.default_display_name = display_name
        request.user.profile.save()

        if first_name or last_name:
            if first_name:
                request.user.first_name = first_name
            if last_name:
                request.user.last_name = last_name
            request.user.save()
        return self.http_response_200({})
