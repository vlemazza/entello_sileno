class MediaItem:
    def __init__(self, file_path="", type=""):
        self.file_path = file_path
        self.type = type


class DownloadResult:
    def __init__(
        self,
        media=None,
        title="",
        content="",
        user="",
        external_url="",
        subreddit="",
        has_media=True,
    ):
        self.media = media or []
        self.title = title
        self.content = content
        self.user = user
        self.external_url = external_url
        self.subreddit = subreddit
        self.has_media = has_media

    def first_media_path(self):
        return self.media[0].file_path if self.media else None

    @staticmethod
    def from_single(file_path, media_type):
        return DownloadResult(media=[MediaItem(file_path=file_path, type=media_type)])
