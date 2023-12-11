import os
import datetime
import dotenv
import isodate
from googleapiclient.discovery import build
from isodate import parse_duration
from src.video import Video

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
            video_id = video["contentDetails"]["videoId"]
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id
            ).execute()
            content_details = video_response['items'][0]['contentDetails']
            duration = content_details.get('duration', '')
            if duration:
                parsed_duration = parse_duration(duration)
                total_duration += parsed_duration

        return total_duration

    def get_video_ids(self):
        videos = self.youtube.playlistItems().list(
            part="contentDetails",
            playlistId=self.playlist_id
        ).execute()['items']

        return [video["contentDetails"]["videoId"] for video in videos]

    def show_best_video(self):
        video_ids = self.get_video_ids()
        list_with_video_info = []
        for video_id in video_ids:
            video_info_dict = {}
            video_obj = Video(video_id)  # инициализация через класс Video
            video_info_dict["likes"] = video_obj.like_count
            video_info_dict["url"] = video_obj.video_url
            list_with_video_info.append(video_info_dict)
        sorted_list = sorted(list_with_video_info, key=lambda x: x["likes"], reverse=True)
        return sorted_list[0]["url"]


def youtube_duration_to_timedelta(duration):
    try:
        return datetime.timedelta(seconds=isodate.parse_duration(duration).total_seconds())
    except (isodate.ISO8601Error, TypeError):
        return datetime.timedelta()
