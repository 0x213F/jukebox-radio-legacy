from django.db.models import Sum

from proj.core.models.querysets import BaseQuerySet


class TrackListingQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Track objects.
    '''

    def from_record(self, record):
        return self.filter(record=record).order_by('number')


    def duration(self):
        return self.aggregate(Sum('track__spotify_duration_ms'))['track__spotify_duration_ms__sum']
