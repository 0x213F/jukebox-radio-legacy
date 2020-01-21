from datetime import datetime
import requests

from cryptography.fernet import Fernet

from django.conf import settings
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Idle streams"

    def handle(self, *args, **options):
        Stream = apps.get_model("music.Stream")
        Comment = apps.get_model("music.Comment")
        Track = apps.get_model("music.Track")
        TrackListing = apps.get_model("music.TrackListing")
        Record = apps.get_model("music.Record")

        now = datetime.now()
        cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)
        streams = Stream.objects.filter(
            Q(
                status=Stream.STATUS_ACTIVATED,
                record_terminates_at__lt=now,
                vote_controlled=True,
            ) | Q(
                status=Stream.STATUS_ACTIVATED,
                record_terminates_at__isnull=True,
                vote_controlled=True,
            )
        )
        for stream in streams:

            # get the oldest item added to the queue
            try:
                comment = Comment.objects.filter(
                    stream=stream,
                    status=Comment.STATUS_QUEUE,
                    record__isnull=True,
                ).order_by('created_at').first()
                print(comment.text)
            except Exception as e:
                continue

            # get the spotify URI of the item added to the queue
            try:
                spotify_uri = comment.text.split('<uri=')[1][:-1]
            except Exception:
                continue

            # look up or create a track that belongs to that URI
            try:
                track = Track.objects.get(spotify_uri=spotify_uri)
            except Exception:
                encrypted_sat = comment.commenter.profile.spotify_access_token
                sat = cipher_suite.decrypt(
                    encrypted_sat.encode("utf-8")
                ).decode("utf-8")
                spotify_id = spotify_uri[14:]

                response = requests.get(
                    f"https://api.spotify.com/v1/tracks/{spotify_id}",
                    headers={
                        "Authorization": f"Bearer {sat}",
                        "Content-Type": "application/json",
                    },
                )
                response_json = response.json()

                spotify_duration_ms = response_json["duration_ms"]

                spotify_name = response_json["name"][:32]
                if len(spotify_name) > 32:
                    spotify_name += "..."

                track = Track.objects.create(
                    spotify_uri=spotify_uri,
                    spotify_duration_ms=spotify_duration_ms,
                    spotify_name=spotify_name,
                )

            # look up an album that only has that track on it
            record_candidates = TrackListing.objects.filter(
                number=1,
                track__spotify_uri=spotify_uri,
            )
            record = None
            for record_candidate in record_candidates:
                rc = record_candidate.record
                tracklisting_count = TrackListing.objects.filter(record=rc).count()
                if tracklisting_count == 1:
                    record = rc
                    break
            if not record:
                record = Record.objects.create(
                    name=f'[Single] {track.spotify_name} #hide'
                )
                TrackListing.objects.create(
                    track=track,
                    record=record,
                    number=1,
                )

            # spin that album!
            try:
                Stream.objects.spin(record, stream)
            except Exception:
                pass

            comment.record = record
            comment.save()
