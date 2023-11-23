import json
from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""
        self.channel_id: str = channel_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(
            id=self.channel_id, part='snippet,statistics'
        ).execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
