from datetime import datetime
from datetime import timedelta

from proj.core.models.querysets import BaseQuerySet


class CommentQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Comment objects.
    '''

    def recent(self, stream):
        '''
        Get a stream's recent comments.
        '''
        now = datetime.now()
        return (
            self
            .select_related('commenter_ticket')
            .filter(
                created_at__gte=now - timedelta(hours=2),
                stream=stream,
            )
            .order_by('created_at')
        )

    def latest_comment(self, user, stream):
        '''
        Get a user's latest comment in a stream.
        '''
        Comment = self.model

        latest_comment = (
            self.filter(stream_id=stream.id).order_by('-created_at').first()
        )

        if not latest_comment:
            raise Comment.DoesNotExist

        return latest_comment
