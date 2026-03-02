import json
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem

class FacebookDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()
        #self.set_cookies_from_env("FB_COOKIES_FILE", "Facebook")

    async def fetch_post(self, url):
        video_path = await self.download_video(url, impersonate=True)
        data = json.loads(self.get_info_ytdlp(url))
        return DownloadResult(
            media=[MediaItem(file_path=video_path, type="video")],
            title=data.get("title") or "Facebook Video",
            description=data.get("description") or "",
            author=(data.get("uploader") or "").strip(),
        )
