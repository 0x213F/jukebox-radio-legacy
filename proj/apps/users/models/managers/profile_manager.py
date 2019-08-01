
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
