from proj.core.views import BaseView


class SignUpView(BaseView):
    def get(self, request, **kwargs):
        return self.template_response(request, 'signup.html')
