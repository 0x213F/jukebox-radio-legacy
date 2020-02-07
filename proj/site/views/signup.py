from django.template.response import TemplateResponse

from proj.core.views import BaseView


class SignUpView(BaseView):
    def get(self, request, **kwargs):
        return TemplateResponse(request, "signup.html")
