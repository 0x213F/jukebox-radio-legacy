from proj.core.views import BaseView


class SignUpView(BaseView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated and request.user.profile.activated_at:
            return self.redirect_response('/')
        return self.template_response(request, 'signup.html')
