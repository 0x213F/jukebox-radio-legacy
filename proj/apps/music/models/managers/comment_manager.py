
import uuid

from datetime import datetime

from proj.core.models.managers import BaseManager



class CommentManager(BaseManager):
    '''
    Django Manager used to manage Comment objects.
    '''

    def validate_create_comment_request(self, user, payload):
        Comment = self.model
        return Comment.RESULT_TRUE

    async def validate_create_comment_request_async(self, user, payload):
        Comment = self.model
        return Comment.RESULT_TRUE

    # TODO: get showing from cache (clean up on terminate showing)
    # TODO: showing_timestamp
    # TODO: track_id
    # TODO: track_timestamp
    async def create_from_payload_async(self, user, payload, _cache):
        from proj.apps.music.models import Showing
        from proj.apps.music.models import Ticket
        Comment = self.model

        if 'showing' not in _cache:
            _cache['showing'] = (
                Showing.objects
                .get(uuid=payload['showing_uuid'])
            )
        showing = _cache['showing']

        if 'ticket' not in _cache:
            _cache['ticket'] = (
                Ticket.objects
                .get(holder_id=user.id, showing_id=showing.id)
            )
        ticket = _cache['ticket']

        if showing.status == Showing.STATUS_TERMINATED:
            raise RuntimeError('Cannot comment on a terminated showing.')
        now = datetime.utcnow()
        status = payload['status'] if showing.status != 'scheduled' else Comment.STATUS_WAITED
        comment = self.model.objects.create(
            status=payload['status'],
            text=payload['text'],
            commenter_id=user.id,
            showing_id=showing.id,
            showing_timestamp=now - showing.showtime_scheduled.replace(tzinfo=None),
            track_id=None,
            track_timestamp=now - showing.showtime_scheduled.replace(tzinfo=None),  # TODO
        )
        _cache['comment'] = comment

    # TODO: showing_timestamp
    # TODO: track_id
    # TODO: track_timestamp
    def serialize(self, comment, ticket):
        return {
            'created_at': comment.created_at.isoformat(),
            'status': comment.status,
            'text': comment.text,
            'commenter': {
                'profile': {
                    'display_name': ticket.display_name,
                    'display_uuid': str(ticket.display_uuid),
                }
            },
            'showing_uuid': str(comment.showing.uuid),
            'showing_timestamp': comment.showing_timestamp.total_seconds(),
            'track': None,
            'track_timestamp': None,
        }
