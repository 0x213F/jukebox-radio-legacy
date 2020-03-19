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
    '''
    Django Manager used to manage Comment objects.
    '''

    async def create_from_payload_async(self, user, payload, *, _cache=None, stream=None, ticket=None):
        '''
        Create a comment from a user's channels payload.
        '''
        Comment = apps.get_model('music', 'Comment')
        Stream = apps.get_model('music', 'Stream')
        Ticket = apps.get_model('music', 'Ticket')
        Profile = apps.get_model('users', 'Profile')

        now = datetime.utcnow()

        text = payload["text"]

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

        return await database_sync_to_async(Comment.objects.create)(
            status=Comment.STATUS_MID_HIGH,
            text=text,
            commenter=user,
            stream=stream,
            track=track,  # TODO
            track_timestamp=track_timestamp,
            commenter_ticket=ticket,
        )

    def serialize(self, comment, ticket=None):
        Stream = apps.get_model('music', 'Stream')
        Ticket = apps.get_model('music', 'Ticket')
        Track = apps.get_model('music', 'Track')

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
            ),
        }
