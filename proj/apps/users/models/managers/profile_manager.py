
import uuid

from datetime import datetime

from django.db.models import Case
from django.db.models import Value
from django.db.models import When

from proj.core.models.managers import BaseManager


class ProfileManager(BaseManager):
    '''
    Django Manager used to query Profile objects.
    '''

    def serialize_user(self, user, active_ticket=None):
        other_fields = {}
        if active_ticket:
            other_fields['active_showing'] = {
                'uuid': user.profile.active_showing_uuid,
                'display_name': active_ticket.display_name,
                'display_uuid': active_ticket.display_uuid,
            }

        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'profile': {
                'display_name': user.profile.default_display_name,
                'has_spotify': bool(user.profile.spotify_scope),
            },
            **other_fields
        }

    async def leave_showing_async(self, user):
        Profile = self.model
        Profile.objects.filter(user_id=user.id).update(
            active_showing_uuid=None,
            display_uuid=None,
        )

    async def join_showing_async(self, user, payload, *, _cache=None):
        from proj.apps.music.models import Showing
        from proj.apps.music.models import Ticket

        showing = Showing.objects.get(uuid=payload['showing_uuid'])
        _cache['showing'] = showing

        user.profile.active_showing_uuid = showing.uuid
        user.profile.save()

        ticket, _ = Ticket.objects.get_or_create(
            holder=user,
            showing=showing,
            defaults={
                'timestamp_last_active': datetime.utcnow(),
                'display_name': user.profile.default_display_name or 'Default',
                'display_uuid': uuid.uuid4(),
            }
        )
        _cache['ticket'] = ticket
