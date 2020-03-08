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

        if not ticket:
            ticket = comment.commenter_ticket

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
