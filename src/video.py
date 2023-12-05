
class Video:
    def __init__(self, video_id, title='Unknown Video', video_link='', views=0, likes=0):
        self.video_id = video_id
        self.title = title
        self.video_link = video_link
        self.views = views
        self.likes = likes

    def __str__(self):
        return f'{self.title} ({self.video_id})'


class PLVideo:
    def __init__(self, video_id, playlist_id, title='Unknown Video', video_link='', views=0, likes=0):
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.title = title
        self.video_link = video_link
        self.views = views
        self.likes = likes

    def __str__(self):
        return f'{self.title} ({self.video_id}) in Playlist {self.playlist_id}'
