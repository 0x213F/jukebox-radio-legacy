
import json
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
        '''
        Serialize the user fields along with:

        - It's profile.
        - List of active showings (just 1 for now).
        '''
        other_profile_fields = {}
        if active_ticket:
            other_profile_fields['showings'] = [
                {
                    'showing_is_administrator': active_ticket.is_administrator,
                    'showing_uuid': user.profile.active_showing_uuid,
                    'display_name': active_ticket.display_name,
                    'display_uuid': active_ticket.display_uuid,
                }
            ]

        scopes = {
            'spotify': bool(user.profile.spotify_scope),
            'apple_music': False,
            'file_system': False,
        }

        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'profile': {
                'display_name': user.profile.default_display_name,
                'scopes': scopes,
                **other_profile_fields
            },
        }

    async def leave_showing_async(self, user):
        '''
        - Update the user's active showing on their profile.
        '''
        Profile = self.model
        Profile.objects.filter(user_id=user.id).update(
            active_showing_uuid=None,
        )



    async def join_showing_async(self, user, showing_uuid, *, _cache=None):
        '''
        After getting the active showing by UUID:

        - Update the user's active showing on their profile.
        - Create or create a ticket record for the user.
        '''
        from proj.apps.music.models import Showing
        from proj.apps.music.models import Ticket

        _cache = self._get_or_fetch_from_cache(
            _cache,
            'showing',
            fetch_func=Showing.objects.get,
            fetch_kwargs={'uuid': showing_uuid}
        )
        showing = _cache['showing']

        user.profile.active_showing_uuid = showing.uuid
        user.profile.save()

        _cache = self._get_or_fetch_from_cache(
            _cache,
            'ticket',
            fetch_func=Ticket.objects.get_or_create,
            fetch_kwargs={
                'holder': user,
                'showing': showing,
                'defaults': {
                    'timestamp_last_active': datetime.utcnow(),
                    'display_name': user.profile.default_display_name or 'Default',
                    'display_uuid': uuid.uuid4(),
                }
            }
        )

        return _cache
