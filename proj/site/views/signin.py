from proj.core.views import BaseView


class SignInView(BaseView):
    def get(self, request, **kwargs):
        return self.template_response(request, 'signin.html')
