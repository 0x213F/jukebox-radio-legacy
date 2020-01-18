import json
import uuid

from datetime import datetime

from channels.db import database_sync_to_async

from random_username.generate import generate_username

from django.apps import apps
from django.db.models import Case
from django.db.models import Value
from django.db.models import When

from proj.core.models.managers import BaseManager
from proj.core.resources.cache import _get_or_fetch_from_cache


class ProfileManager(BaseManager):
    """
    Django Manager used to query Profile objects.
    """

    def serialize_user(self, user, active_ticket=None, active_stream=None):
        """
        Serialize the user fields along with:

        - It's profile.
        - List of active streams.
        """
        Ticket = apps.get_model("music.Ticket")
        Stream = apps.get_model("music.Stream")

        active_ticket = active_ticket or {}

        scopes = {
            "spotify": bool(user.profile.spotify_scope),
        }

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "profile": {
                "active_stream_ticket": Ticket.objects.serialize(active_ticket),
                "scopes": scopes,
                "active_stream": Stream.objects.serialize(active_stream),
                "active_stream_uuid": user.profile.active_stream_uuid,
                "default_name": user.profile.default_display_name,
            },
        }

    async def leave_stream_async(self, user):
        """
        - Update the user's active stream on their profile.
        """
        Profile = self.model
        profile = await database_sync_to_async(Profile.objects.get)(user_id=user.id)
        profile.active_stream_uuid = None
        await database_sync_to_async(profile.save)()

    async def join_stream_async(self, user, stream_uuid, *, _cache=None):
        """
        After getting the active stream by UUID:

        - Update the user's active stream on their profile.
        - Create or create a ticket record for the user.
        """
        from proj.apps.music.models import Stream
        from proj.apps.music.models import Ticket

        Profile = apps.get_model("users.Profile")

        _cache = await _get_or_fetch_from_cache(
            _cache,
            "stream",
            fetch_func=Stream.objects.get,
            fetch_kwargs={"uuid": stream_uuid},
        )
        stream = _cache["stream"]

        _cache = await _get_or_fetch_from_cache(
            _cache,
            "profile",
            fetch_func=Profile.objects.get,
            fetch_kwargs={"user": user},
        )

        profile = _cache["profile"]
        profile.active_stream_uuid = stream.uuid
        await database_sync_to_async(profile.save)()

        _cache = await _get_or_fetch_from_cache(
            _cache,
            "ticket",
            fetch_func=Ticket.objects.get_or_create,
            fetch_kwargs={
                "holder": user,
                "stream": stream,
                "defaults": {
                    "timestamp_last_active": datetime.utcnow(),
                    "holder_name": profile.default_display_name
                    or generate_username(1)[0],
                    "holder_uuid": uuid.uuid4(),
                },
            },
        )

        return _cache
