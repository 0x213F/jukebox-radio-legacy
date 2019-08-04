
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
            }
        }

    async def leave_showing(self, user):
        Profile = self.model
        Profile.objects.filter(user_id=user.id).update(
            active_showing_uuid=None,
            display_uuid=None,
        )

    async def join_showing(self, user, showing):
        from proj.apps.music.models import Ticket
        from proj.apps.users.models import Profile
        from proj.apps.music.models import Showing
        Ticket.objects.get_or_create(
            holder_id=user.id,
            showing_id=showing.id,
            defaults={
                'timestamp_last_active': datetime.utcnow(),
                'display_name': user.profile.display_name or 'default name',
            }
        )
        Profile.objects.filter(user_id=user.id).update(
            active_showing_uuid=showing.uuid,
            display_uuid=Case(
                When(display_uuid=showing.uuid, then=Value(showing.uuid)),
                default=Value(uuid.uuid4()),
            ),
        )
