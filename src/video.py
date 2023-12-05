import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Video:

    def __init__(self, video_id, title='Unknown Video', video_link='', views=0, likes=0):
        self.video_id = video_id
        self.title = title
        self.video_link = video_link
        self.views = views
        self.likes = likes

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id, title='Unknown Video', video_link='', views=0, likes=0):
        super().__init__(video_id, title, video_link, views, likes)
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.title} in Playlist {self.playlist_id}'


def fetch_video_info(video_id, api_key):
    api_key = os.getenv('YT_API_KEY')
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'items' in data and data['items']:
        item = data['items'][0]
        snippet = item['snippet']
        statistics = item['statistics']
        title = snippet['title']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        views = int(statistics.get('viewCount', 0))
        likes = int(statistics.get('likeCount', 0))
        return title, video_link, views, likes
    else:
        return 'Unknown Video', '', 0, 0

