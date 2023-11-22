from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str, api_key: str) -> None:
        """Экземпляр инициализируется id канала и API-ключом."""
        self.api_key = api_key
        self.channel_id = channel_id
        self.name = None
        self.subscribers_count = None

    def fetch_channel_info(self) -> None:
        """Метод для загрузки информации о канале из API."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        channel = youtube.channels().list(
            id=self.channel_id, part='snippet,statistics'
        ).execute()

        if 'items' in channel and channel['items']:
            channel_data = channel['items'][0]
            self.name = channel_data['snippet']['title']
            self.subscribers_count = channel_data[
                'statistics']['subscriberCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        if self.name is None or self.subscribers_count is None:
            self.fetch_channel_info()

        print(f"Имя канала: {self.name}")
        print(f"Количество подписчиков: {self.subscribers_count}")
