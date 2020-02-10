from cryptography.fernet import Fernet
from datetime import datetime
import requests
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime
from random_username.generate import generate_username

from django.apps import apps

from proj.core.views import BaseView


@method_decorator(login_required, name="dispatch")
class CreateRecordView(BaseView):

    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Track = apps.get_model("music.Track")
        TrackListing = apps.get_model("music.TrackListing")
        Record = apps.get_model("music.Record")

        record_name = request.POST.get("record_name", None)

        # create record
        record = Record.objects.create(
            name=record_name,
            user=request.user,
        )

        track_count = 1
        while True:
            spotify_uri = request.POST.get(f"spotify_uri_{track_count}", None)

            if not spotify_uri:
                break

            # already have a track obj
            try:
                track_that_already_exists = Track.objects.get(spotify_uri=spotify_uri)
                if track_that_already_exists:
                    track = track_that_already_exists
                    # if not Record.objects.can_add_track(record, track.spotify_duration_ms):
                    #     break

                    TrackListing.objects.create(
                        record=record, track=track, number=track_count-1,
                    )
                    continue
            except Exception:
                pass

            # we gotta create the track obj
            cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)
            spotify_access_token = cipher_suite.decrypt(
                request.user.profile.spotify_access_token.encode("utf-8")
            ).decode("utf-8")
            spotify_id = spotify_uri[14:]

            response = requests.get(
                f"https://api.spotify.com/v1/tracks/{spotify_id}",
                headers={
                    "Authorization": f"Bearer {spotify_access_token}",
                    "Content-Type": "application/json",
                },
            )
            response_json = response.json()

            spotify_duration_ms = response_json["duration_ms"]

            # if not Record.objects.can_add_track(record, spotify_duration_ms):
            #     break

            spotify_name = response_json["name"][:32]
            if len(response_json["name"]) > 32:
                spotify_name += "..."

            track = Track.objects.create(
                spotify_uri=spotify_uri,
                spotify_name=spotify_name,
                spotify_duration_ms=spotify_duration_ms,
            )

            TrackListing.objects.create(
                record=record, track=track, number=track_count-1,
            )

        return self.http_response({})
