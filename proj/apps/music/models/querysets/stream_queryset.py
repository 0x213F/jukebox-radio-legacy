from proj.core.models.querysets import BaseQuerySet

from django.apps import apps
from django.db.models import Exists
from django.db.models import OuterRef


class StreamQuerySet(BaseQuerySet):
    '''
    Django QuerySet used to query Stream objects.
    '''

    def list_streams(self):
        '''
        QuerySet of stream objects that a user can access.
        '''
        Stream = apps.get_model('music', 'Stream')
        return self.filter(status=Stream.STATUS_ACTIVATED)

    def list_broadcasting_streams(self, user):
        '''
        QuerySet of stream objects that a user can access.
        '''
        Ticket = apps.get_model('music', 'Ticket')
        return self.filter(
            Exists(
                Ticket.objects.filter(
                    stream_id=OuterRef('id'), email=user.email, is_administrator=True,
                )
            )
        )

    def list_tune_in_streams(self, user):
        '''
        QuerySet of stream objects that a user can access.
        '''
        Ticket = apps.get_model('music', 'Ticket')
        return (
            self.list_streams()
            .exclude(
                Exists(
                    Ticket.objects.filter(
                        stream_id=OuterRef('id'),
                        email=user.email,
                        is_administrator=True,
                    )
                )
            )
            .exclude(is_private=True)
        )
