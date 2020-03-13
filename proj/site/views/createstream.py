from proj.core.views import BaseView


class CreateStreamView(BaseView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated or not request.user.profile.is_active:
            return self.redirect_response('/')
        return self.template_response(request, 'createstream.html')
