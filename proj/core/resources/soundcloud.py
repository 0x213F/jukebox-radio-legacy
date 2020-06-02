import requests
import soundcloud

from proj import secrets


class SoundCloud(object):
    @classmethod
    def search_library(cls, query):

        # create a client object with your app credentials
        client = soundcloud.Client(client_id=secrets.SOUNDCLOUD_CLIENT_ID)

        # find all sounds of buskers licensed under 'creative commons share alike'
        tracks = client.get("/tracks", q=query)

        print(tracks)

        raise Exception("ok")
