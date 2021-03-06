from datetime import datetime, timedelta

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Idle streams"

    def handle(self, *args, **options):
        Stream = apps.get_model("music.Stream")

        now = datetime.now()

        streams_to_idle = Stream.objects.filter(
            Q(
                status=Stream.STATUS_ACTIVATED,
                record_terminates_at__lt=now - timedelta(minutes=2),
                updated_at__lt=now - timedelta(minutes=2),
            )
            | Q(
                status=Stream.STATUS_ACTIVATED,
                record_terminates_at__isnull=True,
                updated_at__lt=now - timedelta(minutes=2),
            )
        )
        streams_to_idle.update(status=Stream.STATUS_IDLE)
