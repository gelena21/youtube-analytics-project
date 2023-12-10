import os
import datetime
import dotenv
import isodate
from googleapiclient.discovery import build
from isodate import parse_duration

dotenv.load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = self.build_youtube_service()
        self.playlist_info = self.get_playlist_info()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def build_youtube_service(self):
        return build('youtube', 'v3', developerKey=self.api_key)

    def get_playlist_info(self):
        request = self.youtube.playlists().list(
            part="snippet",
            id=self.playlist_id
        )
        response = request.execute()
        return response['items'][0]['snippet']

    @property
    def title(self):
        return self.playlist_info['title']

    @property
    def link(self):
        return f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        videos = self.youtube.playlistItems().list(
            part="contentDetails",
            playlistId=self.playlist_id
        ).execute()['items']

        total_duration = datetime.timedelta()
        for video in videos:
            content_details = video.get('contentDetails', {})
            duration = content_details.get('duration', '')
            if duration:
                parsed_duration = parse_duration(duration)
                total_duration += parsed_duration

        return total_duration

    def show_best_video(self):
        videos = self.youtube.playlistItems().list(
            part="snippet",
            playlistId=self.playlist_id
        ).execute()['items']

        best_video = max(videos, key=lambda video: video['snippet']['likeCount'])
        return f"https://www.youtube.com/watch?v={best_video['snippet']['resourceId']['videoId']}"


def youtube_duration_to_timedelta(duration):
    try:
        return datetime.timedelta(seconds=isodate.parse_duration(duration).total_seconds())
    except (isodate.ISO8601Error, TypeError):
        return datetime.timedelta()
