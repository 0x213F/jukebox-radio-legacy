from datetime import datetime
from datetime import timedelta

from proj.core.models.querysets import BaseQuerySet


class CommentQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Comment objects.
    '''

    async def list_comments_async(self, stream, most_recent_comment_timestamp):
        '''
        List 100 most recent comments in a stream.
        '''
        Comment = self.model
        qs = Comment.objects.select_related(
            'commenter', 'commenter__profile', 'commenter_ticket',
        )
        qs = qs.filter(stream_id=stream.id)
        if most_recent_comment_timestamp:
            qs = qs.filter(created_at__gt=most_recent_comment_timestamp)
        qs = qs.order_by('created_at')
        return qs[:100]

    def recent(self, stream_uuid):
        '''
        Get a stream's recent comments.
        '''
        now = datetime.now()
        return (
            self
            .select_related('commenter_ticket')
            .filter(
                created_at__gte=now - timedelta(hours=24),
                stream__uuid=stream_uuid,
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
