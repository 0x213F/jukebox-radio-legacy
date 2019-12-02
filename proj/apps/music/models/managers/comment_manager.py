
import uuid

from datetime import datetime

from django.apps import apps

from proj.core.models.managers import BaseManager
from proj.core.fns import results


class CommentManager(BaseManager):
    '''
    Django Manager used to manage Comment objects.
    '''

    async def validate_create_comment_payload_async(
        self, user, payload, _cache=None
    ):
        '''
        Validate a user's channels payload to create a comment.
        '''
        Showing = apps.get_model('music.Showing')
        Comment = self.model

        _cache = self._get_or_fetch_from_cache(
            _cache,
            'showing',
            fetch_func=Showing.objects.get,
            fetch_kwargs={'uuid': payload['showing_uuid']}
        )
        showing = _cache['showing']

        try:
            comment = Comment.objects.latest_comment(user, showing)
            if (
                (comment.status == Comment.STATUS_LEFT) and
                (payload['status'] != Comment.STATUS_JOINED)
            ):
                # Can only join after leaving a showing.
                return results.RESULT_FAILED_VALIDATION, _cache
            elif (
                (comment.status != Comment.STATUS_LEFT) and
                (payload['status'] == Comment.STATUS_JOINED)
            ):
                # Refresh the comments if re-joining
                return (
                    results.RESULT_PERFORM_SIDE_EFFECT_ONLY,
                    _cache
                )
        except Comment.DoesNotExist:
            pass

        return results.RESULT_TRUE, _cache

    async def create_from_payload_async(self, user, payload, *, _cache=None):
        '''
        Create a comment from a user's channels payload.
        '''
        from proj.apps.music.models import Showing
        from proj.apps.music.models import Ticket
        Comment = self.model

        now = datetime.utcnow()

        _cache = self._get_or_fetch_from_cache(
            _cache,
            'showing',
            fetch_func=Showing.objects.get,
            fetch_kwargs={'uuid': payload['showing_uuid']}
        )
        showing = _cache['showing']

        if showing.status == Showing.STATUS_TERMINATED:
            raise RuntimeError('Cannot comment on a terminated showing.')

        _cache = self._get_or_fetch_from_cache(
            _cache,
            'ticket',
            fetch_func=Ticket.objects.get,
            fetch_kwargs={'holder_id': user.id, 'showing_id': showing.id}
        )
        ticket = _cache['ticket']

        status = payload['status']

        comment = Comment.objects.create(
            status=status,
            text=payload['text'],
            commenter_id=user.id,
            showing_id=showing.id,
            track_id=None,  # TODO
            commenter_ticket=ticket,
        )
        self._set_cache(_cache, 'comment', comment)

        return _cache

    # TODO: track_id
    def serialize(self, comment):
        commenter = None
        comment_obj = {
            'id': comment.id,
            'created_at': comment.created_at.isoformat(),
            'status': comment.status,
            'text': comment.text,
            'showing_uuid': str(comment.showing.uuid),
            'track': None,
        }
        if comment.commenter and comment.commenter_ticket:
            comment_obj['commenter'] = {
                'ticket_holder_name': comment.commenter_ticket.holder_name,
                'ticket_holder_uuid': str(comment.commenter_ticket.holder_uuid),
            }
        return comment_obj
