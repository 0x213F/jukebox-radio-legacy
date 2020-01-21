import json
import requests
import uuid
from cryptography.fernet import Fernet

from datetime import datetime

from django.apps import apps
from django.conf import settings

from channels.db import database_sync_to_async

from proj.core.models.managers import BaseManager
from proj.core.fns import results
from proj.core.resources.cache import _set_cache
from proj.core.resources.cache import _get_or_fetch_from_cache


class CommentManager(BaseManager):
    """
    Django Manager used to manage Comment objects.
    """

    async def validate_create_comment_payload_async(self, user, payload, _cache=None):
        """
        Validate a user's channels payload to create a comment.
        """
        Stream = apps.get_model("music.Stream")
        Comment = self.model

        _cache = await _get_or_fetch_from_cache(
            _cache,
            "stream",
            fetch_func=Stream.objects.get,
            fetch_kwargs={"uuid": payload["stream_uuid"]},
        )
        stream = _cache["stream"]

        try:
            comment = await database_sync_to_async(Comment.objects.latest_comment)(
                user, stream
            )
            if (comment.status == Comment.STATUS_LEFT) and (
                payload["status"] != Comment.STATUS_JOINED
            ):
                # Can only join after leaving a stream.
                return results.RESULT_FAILED_VALIDATION, _cache
            elif (comment.status != Comment.STATUS_LEFT) and (
                payload["status"] == Comment.STATUS_JOINED
            ):
                # Refresh the comments if re-joining
                return (results.RESULT_PERFORM_SIDE_EFFECT_ONLY, _cache)
        except Comment.DoesNotExist:
            pass

        return results.RESULT_TRUE, _cache

    async def create_from_payload_async(self, user, payload, *, _cache=None):
        """
        Create a comment from a user's channels payload.
        """
        from proj.apps.music.models import Stream
        from proj.apps.music.models import Ticket

        Profile = apps.get_model('users', 'Profile')

        Comment = self.model

        now = datetime.utcnow()

        _cache = await _get_or_fetch_from_cache(
            _cache,
            "stream",
            fetch_func=Stream.objects.get,
            fetch_kwargs={"uuid": payload["stream_uuid"]},
        )
        stream = _cache["stream"]

        _cache = await _get_or_fetch_from_cache(
            _cache,
            "ticket",
            fetch_func=Ticket.objects.get,
            fetch_kwargs={"holder_id": user.id, "stream_id": stream.id},
        )
        ticket = _cache["ticket"]

        status = payload["status"]

        cmt = None
        track = None
        track_timestamp = None
        try:
            cmt = await database_sync_to_async(
                Comment.objects.select_related("track")
                .filter(
                    created_at__lte=now, stream=stream, status=Comment.STATUS_START,
                )
                .order_by("-created_at")
                .first
            )()
            track = cmt.track
            track_timestamp = now - cmt.created_at.replace(tzinfo=None)
        except Exception as e:
            pass

        commands = (
            '/play ',
            '/undo ',
        )
        text = payload["text"]
        if not text:
            pass
        else:
            text_subsr = text[0:6]
            if stream.vote_controlled and (ticket.is_administrator or user.is_superuser):
                if text_subsr == '/play ':
                    query = text[6:]
                    data = {
                        'q': query,
                        'type': 'track',
                    }

                    _cache = await _get_or_fetch_from_cache(
                        _cache,
                        "profile",
                        fetch_func=Profile.objects.get,
                        fetch_kwargs={"user": user},
                    )
                    profile = _cache["profile"]

                    cipher_suite = Fernet(settings.DATABASE_ENCRYPTION_KEY)

                    user_spotify_access_token = cipher_suite.decrypt(
                        profile.spotify_access_token.encode("utf-8")
                    ).decode("utf-8")

                    response = requests.get(
                        "https://api.spotify.com/v1/search",
                        params=data,
                        headers={
                            "Authorization": f"Bearer {user_spotify_access_token}",
                            "Content-Type": "application/json",
                        },
                    )

                    response_json = response.json()
                    spotify_track_info = response_json['tracks']['items'][0]

                    track_name = spotify_track_info['name']
                    artist_names = ', '.join([
                        artist['name']
                        for artist in spotify_track_info['album']['artists']
                    ])
                    uri = spotify_track_info['uri']
                    text += (
                        '\n\n'
                        f'[System] Adding to queue "{track_name}" '
                        f'by "{artist_names}" <uri={uri}>'
                    )
                    status = Comment.STATUS_QUEUE


        comment = await database_sync_to_async(Comment.objects.create)(
            status=status,
            text=text,
            commenter=user,
            stream=stream,
            track=track,  # TODO
            track_timestamp=track_timestamp,
            commenter_ticket=ticket,
        )
        _set_cache(_cache, "comment", comment)

        return _cache

    def serialize(self, comment, ticket=None):
        Stream = apps.get_model("music.Stream")
        Ticket = apps.get_model("music.Ticket")
        Track = apps.get_model("music.Track")
        return {
            "id": comment.id,
            "created_at": comment.created_at.isoformat(),
            "status": comment.status,
            "text": comment.text,
            "stream": comment.stream_id,  # Stream.objects.serialize(comment.stream),
            "track": comment.track_id,  # Track.objects.serialize(comment.track),
            "ticket": Ticket.objects.serialize(
                ticket
            ),  # Ticket.objects.serialize(comment.commenter_ticket),
        }
