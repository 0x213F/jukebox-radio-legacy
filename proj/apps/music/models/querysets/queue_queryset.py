from proj.core.models.querysets import BaseQuerySet


class QueueQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Queue objects.
    '''

    def get_up_next(self, stream):
        return (
            self.filter(stream=stream, played_at__isnull=True)
            .order_by('created_at').first()
        )
