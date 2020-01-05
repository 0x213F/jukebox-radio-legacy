
from proj.core.models.querysets import BaseQuerySet


class StreamQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Stream objects.
    '''

    def list_streams(self, user):
        '''
        QuerySet of stream objects that a user can access.
        '''
        Stream = self.model
        return (
            self
            .filter(
                status__in=(
                    Stream.STATUS_SCHEDULED,
                    Stream.STATUS_ACTIVATED,
                    Stream.STATUS_IDLE,
                )
            )
        )
