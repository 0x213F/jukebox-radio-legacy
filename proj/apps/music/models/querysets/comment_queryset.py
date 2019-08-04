
from proj.core.models.querysets import BaseQuerySet


class CommentQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Comment objects.
    '''

    async def list_comments_async(self, user, showing, most_recent_comment_timestamp):
        Comment = self.model
        qs = Comment.objects.select_related('commenter', 'commenter__profile')
        qs = qs.filter(showing_id=showing.id)
        if most_recent_comment_timestamp:
            qs = qs.filter(created_at__gte=most_recent_comment_timestamp)
        qs = qs.order_by('created_at')
        return qs[:100]
