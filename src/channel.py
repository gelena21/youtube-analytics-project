class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.api_key = None
        self.channel_id = channel_id
        self.name = None
        self.subscribers_count = None

    def fetch_channel_info(self) -> None:
        """Метод для загрузки информации о канале из API."""
        api_url = f"https://www.googleapis.com/youtube/v3/channels"
        params = {
            'part': 'snippet,statistics',
            'id': self.channel_id,
            'key': self.api_key
        }

        response = requests.get(api_url, params=params)
        data = response.json()

        if 'items' in data and data['items']:
            channel_data = data['items'][0]
            self.name = channel_data['snippet']['title']
            self.subscribers_count = channel_data['statistics']['subscriberCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        if self.name is None or self.subscribers_count is None:
            self.fetch_channel_info()
