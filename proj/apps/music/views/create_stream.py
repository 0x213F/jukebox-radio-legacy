from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


SUBSCRIBED = 'subscribed'
UNSUBSCRIBED = 'unsubscribed'


@method_decorator(login_required, name='dispatch')
class CreateStreamView(BaseView):

    def post(self, request, **kwargs):
        '''
        Update the user's account information.
        '''
        Stream = apps.get_model('music.Stream')
        Ticket = apps.get_model('music.Ticket')

        if not request.user.profile.is_active:
            raise Exception('come on now!')

        stream_name = request.POST.get('name', None)
        tags = request.POST.get('tags', None)

        if len(tags) > 3:
            raise ValueError('Too many emojis')

        tags = ', '.join([char for char in tags])
        if not stream_name or not tags:
            raise Exception('Must provide a stream name')

        now = datetime.now()
        holder_name = request.user.profile.default_display_name or generate_username(1)[0]

        stream = Stream.objects.create(title=stream_name, tags=tags, owner=request.user, owner_name=holder_name, last_status_change_at=now, status=Stream.STATUS_ACTIVATED)
        Ticket.objects.create(
            holder=request.user,
            stream=stream,
            holder_name=holder_name,
            holder_uuid=uuid.uuid4(),
            is_administrator=True,
        )


        return self.http_response({})
