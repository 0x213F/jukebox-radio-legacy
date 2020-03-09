from django.apps import apps

from proj.core.views import BaseView


class QueueView(BaseView):
    def get(self, request, stream, **kwargs):
        Ticket = apps.get_model('music', 'Ticket')
        Stream = apps.get_model('music', 'Stream')

        if not request.user.is_authenticated:
            return self.redirect_response('/')

        ticket = (
            Ticket.objects
            .select_related('stream')
            .get(
                holder=request.user,
                stream__uuid=stream,
                is_administrator=True,
            )
        )
        stream = ticket.stream

        return self.template_response(request, 'queue.html', {
            'stream': stream,
            'should_display_chat_button': False,
            'should_display_volume_button': False,
        })
