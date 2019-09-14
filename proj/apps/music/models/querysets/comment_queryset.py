
from proj.core.models.querysets import BaseQuerySet


class CommentQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Comment objects.
    '''

    async def list_comments_async(
        self, showing, most_recent_comment_timestamp
    ):
        '''
        List 100 most recent comments in a showing.
        '''
        Comment = self.model
        qs = Comment.objects.select_related('commenter', 'commenter__profile')
        qs = qs.filter(showing_id=showing.id)
        if most_recent_comment_timestamp:
            qs = qs.filter(created_at__gt=most_recent_comment_timestamp)
        qs = qs.order_by('created_at')
        return qs[:100]

    def latest_comment(self, user, showing):
        '''
        Get a user's latest comment in a showing.
        '''
        Comment = self.model

        latest_comment = (
            self.filter(showing_id=showing.id).order_by('-created_at')
            .first()
        )

        if not latest_comment:
            raise Comment.DoesNotExist

        return latest_comment
