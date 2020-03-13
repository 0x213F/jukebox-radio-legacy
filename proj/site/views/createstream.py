from proj.core.views import BaseView


class CreateStreamView(BaseView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated or not request.user.profile.activated_at:
            return self.redirect_response('/')
        return self.template_response(request, 'createstream.html')
