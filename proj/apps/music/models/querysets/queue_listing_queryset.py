from datetime import datetime
from django.db.models import Sum
from channels.db import database_sync_to_async

from proj.core.models.querysets import BaseQuerySet


class QueueListingQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query QueueListing objects.
    '''

    def now_playing(self, active_queue):
        now = datetime.now()
        now_playing = self.filter(
            queue=active_queue,
            played_at__lte=now,
        ).order_by('played_at').last()
        if now_playing:
            return now_playing
        return self.filter(
            queue=active_queue,
            played_at__gte=now,
            track_listing__number=1,
        ).get()

    async def now_playing_async(self, active_queue):
        now = datetime.now()
        now_playing = await database_sync_to_async(self.filter(
            queue=active_queue,
            played_at__lte=now,
        ).order_by('played_at').last)()
        if now_playing:
            return now_playing
        now_playing = await database_sync_to_async(self.filter(
            queue=active_queue,
            played_at__gte=now,
            track_listing__number=1,
        ).get)()
        return now_playing

    def up_next(self, active_queue):
        now = datetime.now()
        return (
            self.filter(queue=active_queue, played_at__gt=now)
            .exclude(track_listing__number=1)
            .order_by('track_listing__number')
        )

    async def up_next_async(self, active_queue):
        now = datetime.now()
        up_next = (
            self.filter(queue=active_queue, played_at__gt=now)
            .exclude(track_listing__number=1)
            .order_by('track_listing__number')
        )
        return await database_sync_to_async(list)(up_next)

    def first_from_queue(self, active_queue):
        return (
            self.filter(queue=active_queue)
            .order_by('track_listing__number')
            .first()
        )
