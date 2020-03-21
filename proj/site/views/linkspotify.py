import uuid

from django.apps import apps
from django.contrib.auth import login
from django.contrib.auth.models import User

from proj.core.views import BaseView


class LinkSpotifyView(BaseView):
    def get(self, request, **kwargs):
        Profile = apps.get_model('users', 'Profile')

        stream_uuid = request.GET.get("stream", None)

        is_new_user = False
        if not request.user.is_authenticated:
            uuid_str = str(uuid.uuid4())
            email = f'{uuid_str}@jukebox.radio'
            password = str(uuid.uuid4())

            user = User.objects.create_user(email, email, password)
            Profile.objects.create(
                user=user,
                activated_at=None,
                activated_stream_redirect=stream_uuid,
            )

            login(request, user)
            is_new_user = True

        return self.template_response(
            request,
            'linkspotify.html',
            {'is_new_user': is_new_user}
        )
