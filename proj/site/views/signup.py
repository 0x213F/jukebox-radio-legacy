from proj.core.views import BaseView


class SignUpView(BaseView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated and request.user.profile.is_active:
            return self.redirect_response('/')
        return self.template_response(request, 'signup.html')
