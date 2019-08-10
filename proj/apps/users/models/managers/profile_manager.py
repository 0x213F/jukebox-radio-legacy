
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

    def serialize_user(self, user):
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'profile': {
                'active_showing_uuid': user.profile.active_showing_uuid,
                'display_name': user.profile.display_name,
                'display_uuid': user.profile.display_uuid,
                'has_spotify': bool(user.profile.spotify_scope),
            }
        }

    async def leave_showing(self, user):
        Profile = self.model
        Profile.objects.filter(user_id=user.id).update(
            active_showing_uuid=None,
            display_uuid=None,
        )

    async def join_showing(self, user, showing):
        Profile = self.model
        Profile.objects.filter(user_id=user.id).update(
            active_showing_uuid=showing.uuid,
            display_uuid=Case(
                When(display_uuid=showing.uuid, then=Value(showing.uuid)),
                default=Value(uuid.uuid4()),
            ),
        )
