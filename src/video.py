from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import typing

from helper.youtube_api_manual import video_response

load_dotenv()


class Video:
    API_KEY: str | None = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_title = self.fetch_video_info()["video_title"]
        self.video_url = self.fetch_video_info()["video_url"]
        self.view_count = self.fetch_video_info()["view_count"]
        self.like_count = self.fetch_video_info()["like_count"]

    @classmethod
    def get_service(cls) -> typing.Any:
        """Возвращает объект для работы с API YouTube."""
        service = build('youtube', 'v3', developerKey=cls.API_KEY)
        return service

    def fetch_video_info(self) -> dict:
        """Получает информацию о видео с помощью YouTube API."""
        youtube = self.get_service()
        video_responce: object = (
            youtube.videos().list(part="snippet,statistics,contentDetails,topicDetails", id=self.video_id).execute()
            )
        video_title: str = video_response["items"][0]["snippet"]["title"]
        video_url: str = "https://youtu.be/" + self.video_id
        view_count: int = video_response["items"][0]["statistics"]["viewCount"]
        like_count: int = video_response["items"][0]["statistics"]["likeCount"]
        return {
            "video_title": video_title,
            "view_count": view_count,
            "like_count": like_count,
            "video_url": video_url,
        }
        # youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        # request = youtube.videos().list(part='snippet,statistics', id=self.video_id)
        # response = request.execute()

    #     if 'items' in response and response['items']:
    #         item = response['items'][0]
    #         snippet = item['snippet']
    #         statistics = item['statistics']
    #
    #         title = snippet.get('title', 'Unknown Video')
    #         video_link = f'https://www.youtube.com/watch?v={self.video_id}'
    #         views = int(statistics.get('viewCount', 0))
    #         likes = int(statistics.get('likeCount', 0))
    #
    #         return title, video_link, views, likes
    #     else:
    #         return 'Unknown Video', '', 0, 0
    #
    def __str__(self) -> str:
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
