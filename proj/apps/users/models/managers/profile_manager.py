from channels.db import database_sync_to_async
from django.apps import apps

from proj.core.models.managers import BaseManager


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
            "is_staff": user.is_staff,
            "profile": {
                "active_stream_ticket": Ticket.objects.serialize(active_ticket),
                "scopes": scopes,
                "active_stream": Stream.objects.serialize(active_stream),
                "default_name": user.profile.default_display_name,
            },
        }

    async def leave_stream_async(self, user, ticket, stream):
        """
        - Update the user's active stream on their profile.
        """
        Profile = self.model
        Ticket = apps.get_model("music", "Ticket")

        ticket.is_active = False
        await database_sync_to_async(Ticket.objects.filter(id=ticket.id).update)(
            is_active=False,
            is_speaking=False,
            sent_initialization_segment=False,
            initialization_segment=None,
            partial_block=None,
        )

    async def join_stream_async(self, user, stream_uuid):
        """
        After getting the active stream by UUID:

        - Update the user's active stream on their profile.
        - Create or create a ticket record for the user.
        """
        Stream = apps.get_model("music", "Stream")
        Ticket = apps.get_model("music", "Ticket")
        Profile = apps.get_model("users", "Profile")

        get_stream = Stream.objects.select_related(
            "current_queue",
            "current_queue__record",
            "current_tracklisting",
            "current_tracklisting__track",
        ).get
        stream = await database_sync_to_async(get_stream)(uuid=stream_uuid)

        get_profile = Profile.objects.get
        profile = await database_sync_to_async(get_profile)(user=user)

        await database_sync_to_async(profile.save)()

        get_ticket = Ticket.objects.get
        ticket = await database_sync_to_async(get_ticket)(
            email=user.email, stream=stream
        )

        ticket.is_active = True
        await database_sync_to_async(ticket.save)()

        return stream, ticket, profile
