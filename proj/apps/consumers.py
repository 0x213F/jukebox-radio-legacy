import json
import requests_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from datetime import datetime
from urllib import parse

from proj.apps.music.models import Comment
from proj.apps.music.models import QueueListing
from proj.apps.music.models import Record
from proj.apps.music.models import Stream
from proj.apps.music.models import Ticket
from proj.apps.music.models import Track
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

        # send back recent chat activity
        should_display_comments = url_params["display_comments"] == "true"
        if should_display_comments:
            comments_qs = Comment.objects.select_related("commenter_ticket").recent(
                self.scope["stream"]
            )
            comments = await database_sync_to_async(list)(comments_qs)
            await self.send_update({
                'read': {
                    'comments': [
                        Comment.objects.serialize(c, ticket=c.commenter_ticket)
                        for c in comments
                    ]
                }
            })

        # create db log
        await Comment.objects.create_and_share_comment_async(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            status=Comment.STATUS_JOINED,
        )

        # verify the user has an active spotify token
        try:
            await self.scope["spotify"].get_user_info_async()
        except requests_async.exceptions.HTTPError:
            await self.send_update({'read': {'playback': [{'status': self.PLAY_BAR_AUTHORIZE_SPOITFY}]}})
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

        await Comment.objects.create_and_share_comment_async(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            text=payload["text"],
        )

    # - - - - - -
    # disconnect
    # - - - - - -

    async def websocket_disconnect(self, event):
        await Profile.objects.leave_stream_async(
            self.scope["user"], self.scope["ticket"], self.scope["stream"]
        )
        await self.remove_from_channel()

    # - - - - - - - - - - - -
    # broadcast
    # - - - - - - - - - - - -

    async def send_update(self, data):
        if set(['type', 'text']) == set(data.keys()):
            data = data['text']
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data),
        })

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

    # - - - - - - - - - - - - - -
    #          HELPERS           |
    # - - - - - - - - - - - - - -

    async def websocket_accept(self):
        await self.send({"type": "websocket.accept"})

    async def add_to_channel(self):
        # add to group channel
        await self.channel_layer.group_add(
            self.scope["stream"].chat_room, self.channel_name
        )

        # add to individual channel
        user_id = self.scope['user'].id
        await self.channel_layer.group_add(
            f'user-{user_id}', self.channel_name
        )

    async def remove_from_channel(self):
        # remove from group channel
        await self.channel_layer.group_discard(
            self.scope['stream'].chat_room, self.channel_name
        )

        # remove from individual channel
        user_id = self.scope['user'].id
        await self.channel_layer.group_discard(
            f'user-{user_id}', self.channel_name
        )

        # create db log
        await Comment.objects.create_and_share_comment_async(
            self.scope["user"],
            self.scope["stream"],
            self.scope["ticket"],
            status=Comment.STATUS_LEFT,
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

    #############################

    async def sync_playback(self, onload=False):

        # reload stream object
        # TODO load from cache
        self.scope['stream'] = await database_sync_to_async(
            Stream.objects.select_related(
                'current_queue', 'current_queue__record', 'current_tracklisting', 'current_tracklisting__track'
            ).get
        )(id=self.scope['stream'].id)

        # nothing is happening, come back later
        record_terminates_at = self.scope['stream'].record_terminates_at
        if (
            not record_terminates_at or
            record_terminates_at
            and datetime.now() > record_terminates_at.replace(tzinfo=None)
        ):
            playback_data = {
                'record': None,
                'queuelistings': None,
                'stream': Stream.objects.serialize(self.scope['stream']),
                'status': 'waiting-for-stream-to-start',
            }
            payload = {
                'read': {'playback': [playback_data]},
            }
            await self.send_update(payload)
            return

        # base case: first spin
        current_queue = self.scope['stream'].current_queue
        record = current_queue.record

        if not record.youtube_id:
            current_queue_listing = await QueueListing.objects.select_related('track_listing', 'track_listing__track').now_playing_async(current_queue)
            up_next_qls = await QueueListing.objects.select_related('track_listing', 'track_listing__track').up_next_async(current_queue)
            qls = [QueueListing.objects.serialize(current_queue_listing)]
            qls.extend([QueueListing.objects.serialize(ql) for ql in up_next_qls])

            playback_data = {
                'record': Record.objects.serialize(record),
                'queuelistings': qls,
                'stream': Stream.objects.serialize(self.scope['stream']),
                'status': 'playing_and_synced',
            }
        else:
            playback_data = {
                'record': Record.objects.serialize(record),
                'queuelistings': [],
                'stream': Stream.objects.serialize(self.scope['stream']),
                'status': 'playing_and_synced',
            }

        payload = {
            'read': {'playback': [playback_data]},
        }
        await self.send_update(payload)
