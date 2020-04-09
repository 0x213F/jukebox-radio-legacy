import json
import requests_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from datetime import datetime
from urllib import parse

from proj.apps.music.models import Comment
from proj.apps.music.models import Record
from proj.apps.music.models import Stream
from proj.apps.music.models import Ticket
from proj.apps.users.models import Profile
from proj.core.resources import Spotify


class Consumer(AsyncConsumer):

    # - - - -
    # constants
    # - - - -

    PLAY_BAR_AUTHORIZE_SPOITFY = "authorize-spotify"

    # - - - -
    # helpers
    # - - - -

    def get_data_from_ws_path(self):
        """
        Takes a path from the query_string and parses it into a dict
        """
        ws_path = self.scope["query_string"]
        return dict(parse.parse_qsl(parse.urlsplit(ws_path).path.decode("utf-8")))

    # - - - -
    # connect
    # - - - -

    async def websocket_connect(self, event):

        # accept connection
        await self.websocket_accept()

        # parse data from WSS URL
        url_params = self.get_data_from_ws_path()
        stream_uuid = url_params["uuid"]

        # get user's profile
        self.scope["profile"] = await database_sync_to_async(Profile.objects.get)(
            user=self.scope["user"]
        )

        # init spotify interface
        self.scope["spotify"] = Spotify(
            self.scope["user"], profile=self.scope["profile"]
        )

        # join stream, grab stuff from DB
        (
            self.scope["stream"],
            self.scope["ticket"],
            self.scope["profile"],
        ) = await Profile.objects.join_stream_async(self.scope["user"], stream_uuid,)

        # add to channel
        await self.add_to_channel()
        user_id = self.scope["user"].id
        await self.channel_layer.group_add(f"user-{user_id}", self.channel_name)

        # send back recent chat activity
        should_display_comments = url_params["display_comments"] == "true"
        if should_display_comments:
            comments_qs = Comment.objects.select_related("commenter_ticket").recent(
                self.scope["stream"]
            )
            comments = await database_sync_to_async(list)(comments_qs)
            await self.send_comments(comments)

        # verify the user has an active spotify token
        try:
            await self.scope["spotify"].get_user_info_async()
        except requests_async.exceptions.HTTPError:
            await self.update_playbar(self.PLAY_BAR_AUTHORIZE_SPOITFY)
            return

        # sync playback
        await self.sync_playback(onload=True)

    # - - - - -
    # receieve
    # - - - - -

    async def websocket_receive(self, event):
        payload = json.loads(event["text"])
        # action = payload['action']

        if "resync" in payload:
            await self.sync_playback()
            return

        await Comment.objects.create_and_share_comment(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            text=payload["text"],
        )

    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):

        await Profile.objects.leave_stream_async(self.scope["user"])

        ticket = self.scope["ticket"]

        ticket.is_active = False
        await database_sync_to_async(Ticket.objects.filter(id=ticket.id).update)(
            is_active=False
        )

        await self.remove_from_channel()
        user_id = self.scope["user"].id
        await self.channel_layer.group_discard(f"user-{user_id}", self.channel_name)

        # Create record of comment.
        await Comment.objects.create_and_share_comment(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            status=Comment.STATUS_LEFT,
        )

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def broadcast(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})
        try:
            if bool(event["playback"]) and bool(self.scope["spotify"].token):
                await self.play_tracks(event["playback"])
        except Exception:
            pass

    async def play_tracks(self, playback):
        token = self.scope["spotify"].token
        action = playback["action"]
        data = json.dumps(playback["data"]) or {}
        await requests_async.put(
            f"https://api.spotify.com/v1/me/player/{action}",
            data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

    async def promote_to_host(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({"data": {"promote_to_host": True,}}),
            }
        )

    async def demote_from_host(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({"data": {"promote_to_host": False,}}),
            }
        )

    async def update_queue(self, event):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({"data": {"update_queue": True,}}),
            }
        )

    async def update_name(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})

    # - - - - - - - - - - - - - -
    #          HELPERS           |
    # - - - - - - - - - - - - - -

    async def websocket_accept(self):
        await self.send({"type": "websocket.accept"})

    async def add_to_channel(self):
        await (
            self.channel_layer.group_add(
                self.scope["stream"].chat_room, self.channel_name
            )
        )

        # create db log
        await Comment.objects.create_and_share_comment(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            status=Comment.STATUS_JOINED,
        )

    async def remove_from_channel(self):
        await self.channel_layer.group_discard(
            self.scope["stream"].chat_room, self.channel_name
        )

    async def channel_post_comment(self, comment):
        await self.channel_layer.group_send(
            self.scope["stream"].chat_room,
            {
                "type": "broadcast",
                "text": json.dumps(
                    {
                        "data": {
                            "comments": [
                                Comment.objects.serialize(
                                    comment, ticket=self.scope["ticket"]
                                )
                            ],
                            "playback": {"next_step": "noop",},
                        }
                    }
                ),
            },
        )

    async def update_playbar(self, status):
        stream = Stream.objects.serialize(self.scope["stream"])
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {"data": {"stream": stream, "playback": {"next_step": status,}}}
                ),
            }
        )

    async def send_comments(self, comments):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {
                        "data": {
                            "comments": [
                                Comment.objects.serialize(c, ticket=c.commenter_ticket)
                                for c in comments
                            ],
                            "playback": {"next_step": "noop",},
                        }
                    }
                ),
            }
        )

    async def send_record(self, record):
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {
                        "data": {
                            "record": Record.objects.serialize(record),
                            "playback": {"next_step": "currently-playing",},
                        }
                    }
                ),
            }
        )

    #############################

    async def sync_playback(self, onload=False):
        self.scope["stream"] = await database_sync_to_async(
            Stream.objects.select_related(
                "current_record", "current_tracklisting", "current_tracklisting__track"
            ).get
        )(id=self.scope["stream"].id)

        record_terminates_at = self.scope["stream"].record_terminates_at
        if (
            record_terminates_at
            and datetime.now() > record_terminates_at.replace(tzinfo=None)
            or not record_terminates_at
        ):
            await self.update_playbar("waiting-for-stream-to-start")
            return

        # [7]
        # determine if the user's Spotify is already synced with the stream
        try:
            currently_playing_data = await (
                self.scope["spotify"].get_currently_playing_async()
            )

            spotify_track_duration_ms = currently_playing_data["spotify_ms"]
            spotify_uri = currently_playing_data["spotify_uri"]
            spotify_is_playing = currently_playing_data["spotify_is_playing"]

            ms_since_record_was_played = (
                datetime.now()
                - self.scope["stream"].record_begun_at.replace(tzinfo=None)
            ).total_seconds() * 1000

            try:
                current_tracklisting = await database_sync_to_async(
                    self.scope["stream"].current_record.tracks_through.select_related('track').filter(
                        relative_duration__lte=ms_since_record_was_played
                    ).order_by('relative_duration').last
                )()
                if current_tracklisting:
                    elapsed_track_duration = current_tracklisting.relative_duration
                    current_spotify_uri = current_tracklisting.track.spotify_uri
                else:
                    elapsed_track_duration = -1
                    current_spotify_uri = None
            except Exception:
                elapsed_track_duration = -1
                current_spotify_uri = None

            print(ms_since_record_was_played)
            print(elapsed_track_duration)

            ms_since_track_was_played = (
                datetime.now()
                - self.scope["stream"].record_begun_at.replace(tzinfo=None)
            ).total_seconds() * 1000
            offsync_ms = abs(ms_since_track_was_played - spotify_track_duration_ms - elapsed_track_duration)

            user_is_already_in_sync = (
                elapsed_track_duration != -1 and
                current_spotify_uri and
                spotify_is_playing and
                current_spotify_uri == spotify_uri and
                offsync_ms < 5000
            )

            if user_is_already_in_sync:
                record = self.scope["stream"].current_record
                if onload:
                    await self.send_record(record)
                return

        except Exception:
            # assuming everything is behaving as expected, we assume that the
            # user's Spotify client is disconnected
            await self.update_playbar("spotify-streaming-client-not-found")
            return

        # [8]
        # get the track playing and tracks in the queue
        uris = (
            self.scope["stream"]
            .current_record.tracks_through.all()
            .order_by("number")
            .values_list("track__spotify_uri", flat=True)
        )
        uris = await database_sync_to_async(list)(uris)

        if not uris:
            return

        # [9]
        # sync the user's playback with the stream
        ms_since_track_was_played = (
            datetime.now()
            - self.scope["stream"].record_begun_at.replace(tzinfo=None)
        ).total_seconds() * 1000
        await self.play_tracks(
            {
                "action": "play",
                "data": {"uris": uris, "position_ms": ms_since_track_was_played,},
            }
        )

        # [A]
        # update the front-end with playback status
        record = self.scope["stream"].current_record
        await self.send_record(record)
