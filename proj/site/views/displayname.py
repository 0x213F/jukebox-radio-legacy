import uuid

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps
from django.template.response import TemplateResponse

from proj.core.views import BaseView


class DisplayNameView(BaseView):
    def get(self, request, stream, **kwargs):
        Stream = apps.get_model('music', 'Stream')
        Ticket = apps.get_model('music', 'Ticket')

        stream = Stream.objects.get(uuid=stream)
        ticket = Ticket.objects.get_or_create(holder=request.user, stream=stream, defaults={
            "timestamp_last_active": datetime.utcnow(),
            "holder_name": request.user.profile.default_display_name or generate_username(1)[0],
            "holder_uuid": uuid.uuid4(),
        })[0]

        return TemplateResponse(request, "displayname.html", {'stream': stream, 'ticket': ticket})
