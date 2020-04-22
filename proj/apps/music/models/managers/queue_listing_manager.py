from django.apps import apps

from proj.core.models.managers import BaseManager


class QueueListingManager(BaseManager):
    '''
    Django Manager used to manage QueueListing objects.
    '''

    def serialize(self, queuelisting):
        '''
        Make a QueueListing object JSON serializable.
        '''
        TrackListing = apps.get_model('music', 'TrackListing')
        return {
            'start_at_ms': queuelisting.start_at_ms,
            'end_at_ms': queuelisting.end_at_ms,
            'played_at': queuelisting.played_at.total_seconds() * 1000.0,
            'paused_at': queuelisting.played_at.isoformat(),
            'tracklisting': TrackListing.objects.serialize(queuelisting.track_listing),
        }
