from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import typing


load_dotenv()


class Video:
    API_KEY: str | None = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = None
        self.video_url = None
        self.view_count = None
        self.like_count = None
        self.error_message = None

        try:
            video_info = self.fetch_video_info()
            self.title = video_info["video_title"]
            self.video_url = video_info["video_url"]
            self.view_count = video_info["view_count"]
            self.like_count = video_info["like_count"]
        except Exception as e:
            self.error_message = str(e)

    @classmethod
    def get_service(cls) -> typing.Any:
        """Возвращает объект для работы с API YouTube."""
        service = build('youtube', 'v3', developerKey=cls.API_KEY)
        return service

    def fetch_video_info(self) -> dict:
        """Получает информацию о видео с помощью YouTube API."""
        youtube = self.get_service()
        video_response: object = (
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

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
