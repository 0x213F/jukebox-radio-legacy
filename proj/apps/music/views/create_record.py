from cryptography.fernet import Fernet
from datetime import datetime
import requests
import uuid
from urllib.parse import urlparse

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime
from random_username.generate import generate_username


from proj.core.views import BaseView
from proj.core.resources import Spotify


@method_decorator(login_required, name="dispatch")
class CreateRecordView(BaseView):

    def post(self, request, **kwargs):
        """
        Update the user's account information.
        """
        Track = apps.get_model("music.Track")
        TrackListing = apps.get_model("music.TrackListing")
        Record = apps.get_model("music.Record")

        spotify_link = request.POST.get("spotify_link", None)

        spotify = Spotify(request.user, 'spotify')
        spotify_id = spotify.get_spotify_id_from_spotify_link(spotify_link)

        # get our URIs in order
        if 'track' in spotify_link:
            record_name = ''
            uris = [spotify_link[7:]]
        elif 'album' in spotify_link:
            album_info = spotify.get_album_info(spotify_id, request.user)
            record_name = album_info['album_name']
            uris = album_info['spotify_uris']
        elif 'playlist' in spotify_link:
            record_name = ''
            uris = []
        else:
            raise ValueError(f'Invalid spotify_link: {spotify_link}')


        raise RuntimeError('still working on this...')
        # create record
        record = Record.objects.create(
            name=record_name,
            user=request.user,
        )

        # add tracklistings
        track_count = 0
        for uri in uris:
            track_count += 1

            # already have a track obj
            try:
                track = Track.objects.get(spotify_uri=uri)

            # gotta make a new one
            except Track.DoesNotExist:
                spotify_id = uri[14:]
                response = requests.get(
                    f"https://api.spotify.com/v1/tracks/{spotify_id}",
                    headers={
                        "Authorization": f"Bearer {spotify_access_token}",
                        "Content-Type": "application/json",
                    },
                )
                response_json = response.json()

                spotify_duration_ms = response_json["duration_ms"]
                spotify_name = response_json["name"][:32]
                if len(response_json["name"]) > 32:
                    spotify_name += "..."

                track = Track.objects.create(
                    spotify_uri=spotify_uri,
                    spotify_name=spotify_name,
                    spotify_duration_ms=spotify_duration_ms,
                )

            finally:
                TrackListing.objects.create(
                    record=record, track=track, number=track_count-1,
                )

        return self.http_response({})
