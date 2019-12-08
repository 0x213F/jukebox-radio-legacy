
from datetime import datetime
from datetime import timedelta

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Idle showings'

    def handle(self, *args, **options):
        Showing = apps.get_model('music.Showing')

        now = datetime.now()

        showings_to_idle = (
            Showing
            .objects
            .filter(
                status=Showing.STATUS_ACTIVATED,
                record_terminates_at__lt=now - timedelta(minutes=5),
            )
        )
        showings_to_idle.update(status=Showing.STATUS_IDLE)
