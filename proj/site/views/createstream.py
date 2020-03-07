from proj.core.views import BaseView


class CreateStreamView(BaseView):
    def get(self, request, **kwargs):
        return self.template_response(request, 'createstream.html')
