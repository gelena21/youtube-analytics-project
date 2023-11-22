from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала."""
        self.api_key = os.getenv('YT_API_KEY')
        self.channel_id = channel_id
        self.name = None
        self.subscribers_count = None

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(
            id=self.channel_id, part='snippet,statistics'
        ).execute()

        if 'items' in channel and channel['items']:
            channel_data = channel['items'][0]
            self.name = channel_data['snippet']['title']
            self.subscribers_count = channel_data[
                'statistics']['subscriberCount']

        print(f"Имя канала: {self.name}")
        print(f"Количество подписчиков: {self.subscribers_count}")
