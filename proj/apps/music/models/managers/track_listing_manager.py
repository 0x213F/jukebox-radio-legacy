from proj.core.models.managers import BaseManager


class TrackListingManager(BaseManager):
    '''
    Django Manager used to manage TrackListing objects.
    '''

    def serialize(self, tracklisting):
        '''
        Make a TrackListing object JSON serializable.
        '''
        return {
            'track': {
                'spotify_name': tracklisting.track.spotify_name,
                'spotify_uri': tracklisting.track.spotify_uri,
                'spotify_duration_ms': tracklisting.track.spotify_duration_ms,
            }
        }

    def add_to_record(self, record, tracks):
        '''
        Add some tracks to a record.

        NOTE: we assume that the record has no tracks.
        '''
        TrackListing = self.model
        tls = []

        number = 1
        relative_duration = 0
        for track in tracks:
            tl = TrackListing(
                record=record,
                track=track,
                number=number,
                relative_duration=relative_duration,
            )
            tls.append(tl)
            number += 1
            relative_duration += track.spotify_duration_ms
        TrackListing.objects.bulk_create(tls)
