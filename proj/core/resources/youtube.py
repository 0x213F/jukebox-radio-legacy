import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import requests
from proj import secrets


class YouTube(object):

    detail_url = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=YQHsXMglC9A&key=AIzaSyBuvHd6Q9I4DyXB-TPi-Ki_s7PkXJ9vKJ4'

    headers = [{'Accept', 'application/json'}]

    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

    @classmethod
    def _get_search_url(query):
        return (
            'https://www.googleapis.com/youtube/v3/search?part=snippet&'
            f'q={query}&key={secrets.GOOGLE_API_KEY}'
        )

    @classmethod
    def search_library(cls, query):
        params = {
            'part': 'snippet',
            'q': query,
            'key': secrets.GOOGLE_API_KEY,
            'type': 'video',
            'maxResults': 16,
        }

        response = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params=params,
            headers={
                "Content-Type": "application/json",
            },
        )
        response_json = response.json()

        response_data = []
        for item in response_json['items']:
            youtube_id = item['id']['videoId']
            youtube_channel = item['snippet']['channelTitle']
            youtube_name = item['snippet']['title']
            youtube_img = item['snippet']['thumbnails']['high']['url']
            response_data.append({
                'youtube_id': youtube_id,
                'record_artist': youtube_channel,
                'record_name': youtube_name,
                'record_thumbnail': youtube_img,
            })

        return response_data


    @classmethod
    def get_info(cls, youtube_id):
        params = {
            'part': 'snippet,contentDetails',
            'id': youtube_id,
            'key': secrets.GOOGLE_API_KEY,
        }

        response = requests.get(
            'https://www.googleapis.com/youtube/v3/videos',
            params=params,
            headers={
                "Content-Type": "application/json",
            },
        )

        response_json = response.json()

        # clean duration
        duration_raw = response_json['items'][0]['contentDetails']['duration']
        print(duration_raw)
        duration_minutes_raw = duration_raw[2:].split('M')[0] if 'M' in duration_raw else 0
        duration_seconds_raw = duration_raw.split('M')[1][:-1] if 'M' in duration_raw else duration_raw[2:][:-1]
        duration_ms = (
            (60 * 1000 * int(duration_minutes_raw)) +
            (1000 * int(duration_seconds_raw))
        )

        return {
            'youtube_id': response_json['items'][0]['id'],
            'youtube_name': response_json['items'][0]['snippet']['title'],
            'youtube_duration_ms': duration_ms,
            'youtube_img_high': response_json['items'][0]['snippet']['thumbnails']['high']['url'],
        }
