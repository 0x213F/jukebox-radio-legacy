import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.apps import apps

from proj.core.models.managers import BaseManager

channel_layer = get_channel_layer()


class CommentManager(BaseManager):
    """
    Django Manager used to manage Comment objects.
    """

    def serialize(self, comment):
        """
        Make a Comment object JSON serializable.
        """
        Ticket = apps.get_model("music", "Ticket")

        return {
            "created_at": comment.created_at.isoformat(),
            "status": comment.status,
            "text": comment.text,
            "stream": comment.stream_id,
            "track": comment.track_id,
            "ticket": Ticket.objects.serialize(comment.commenter_ticket),
        }

    async def create_and_share_comment_async(
        self, user, stream, ticket, text=None, status=None
    ):
        """
        Create a record of the user's comment and broadcast it to the stream.
        """
        Comment = apps.get_model("music", "Comment")

        now = datetime.utcnow()
        try:
            # TODO: this is wrong
            track = stream.current_tracklisting.track
            track_timestamp = now - stream.tracklisting_begun_at.replace(tzinfo=None)
        except AttributeError:
            track = None
            track_timestamp = None

        comment = await database_sync_to_async(Comment.objects.create)(
            status=status or Comment.STATUS_COMMENTED,
            text=text,
            commenter=user,
            commenter_ticket=ticket,
            stream=stream,
            record=stream.current_queue and stream.current_queue.record,
            track=track,
            track_timestamp=track_timestamp,
        )

        await channel_layer.group_send(
            stream.chat_room,
            {
                "type": "send_update",
                "text": {"created": {"comments": [Comment.objects.serialize(comment)]}},
            },
        )
