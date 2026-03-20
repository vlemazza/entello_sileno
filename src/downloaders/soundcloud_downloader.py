from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult


class SoundCloudDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()

    async def fetch_audio(self, url):
        info = await self.get_info_from_ytdlp(url)
        result = await self.download_audio(url)
        result.title = info.get("title") or info.get("track") or "SoundCloud Audio"
        result.content = info.get("description") or ""
        result.user = info.get("uploader") or info.get("artist") or ""
        return result
