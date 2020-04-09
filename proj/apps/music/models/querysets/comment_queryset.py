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
            self.select_related('commenter_ticket')
            .filter(created_at__gte=now - timedelta(hours=2), stream=stream,)
            .order_by('created_at')
        )
