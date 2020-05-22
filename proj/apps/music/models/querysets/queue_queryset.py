from proj.core.models.querysets import BaseQuerySet


class QueueQuerySet(BaseQuerySet):
    """
    Django QuerySet used to query Queue objects.
    """

    def delete(self):
        """
        Manually turn off to update all queues up next.
        """
        for queue in self:
            queue.delete()

    def get_up_next(self, stream):
        return (
            self.filter(stream=stream, played_at__isnull=True)
            .order_by("created_at")
            .first()
        )

    def in_stream(self, stream):
        return self.filter(played_at__isnull=True, stream=stream).order_by("created_at")
