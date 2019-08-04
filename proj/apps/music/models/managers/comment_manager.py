
from datetime import datetime

from proj.core.models.managers import BaseManager



class CommentManager(BaseManager):
    '''
    Django Manager used to manage Comment objects.
    '''

    # TODO: get showing from cache (clean up on terminate showing)
    # TODO: showing_timestamp
    # TODO: track_id
    # TODO: track_timestamp
    async def create_from_payload_async(self, user, payload):
        from proj.apps.music.models import Showing
        showing = Showing.objects.get(uuid=payload['showing_uuid'])
        if showing.status == Showing.STATUS_TERMINATED:
            raise RuntimeError('Cannot comment on a terminated showing.')
        now = datetime.utcnow()
        comment = self.model.objects.create(
            status=payload['status'],
            text=payload['text'],
            commenter_id=user.id,
            showing_id=showing.id,
            showing_timestamp=now - showing.showtime_scheduled.replace(tzinfo=None),
            track_id=None,
            track_timestamp=now - showing.showtime_scheduled.replace(tzinfo=None),  # TODO
        )
        return comment, showing

    # TODO: showing_timestamp
    # TODO: track_id
    # TODO: track_timestamp
    def serialize(self, comment):
        return {
            'created_at': comment.created_at.isoformat(),
            'status': comment.status,
            'text': comment.text,
            'commenter': {
                'profile': {
                    'display_name': comment.commenter.profile.display_name,
                    'display_uuid': str(comment.commenter.profile.display_uuid),
                }
            },
            'showing_uuid': str(comment.showing.uuid),
            'showing_timestamp': comment.showing_timestamp.total_seconds(),
            'track': None,
            'track_timestamp': None,
        }
