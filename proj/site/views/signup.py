from proj.core.views import BaseView


class SignUpView(BaseView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated and request.user.profile.activated_at:
            return self.redirect_response('/')
        elif not request.user.is_authenticated:
            return self.template_response(request, 'signup.html', {'redirect_path': '/linkspotify'})
        else:  # user is temp signed in
            return self.template_response(request, 'signup.html', {'redirect_path': '/'})
