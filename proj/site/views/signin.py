from proj.core.views import BaseView


class SignInView(BaseView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return self.redirect_response("/")
        return self.template_response(request, "signin.html")
