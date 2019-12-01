
from proj.core.models.querysets import BaseQuerySet


class ShowingQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Showing objects.
    '''

    def list_showings(self, user):
        '''
        QuerySet of showing objects that a user can access.
        '''
        Showing = self.model
        return (
            self
            .filter(
                status__in=(
                    Showing.STATUS_SCHEDULED,
                    Showing.STATUS_ACTIVATED,
                    Showing.STATUS_IDLE,
                )
            )
        )
