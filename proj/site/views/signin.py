from django.template.response import TemplateResponse

from proj.core.views import BaseView


class SignInView(BaseView):
    def get(self, request, **kwargs):
        return TemplateResponse(request, "signin.html")
