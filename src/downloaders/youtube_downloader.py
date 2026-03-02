import os
import json
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem

class YouTubeDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()
        self.max_duration = int(os.getenv("MAX_DURATION"))
    

    async def download_video(self, url):
        info = json.loads(self.get_info_ytdlp(url))
        duration = info.get('duration', 0)
        if duration > self.max_duration:
            raise ValueError(f"[YouTubeDownloader] video exceeds {self.max_duration}s")

        video_path = await super().download_video(url)
        return DownloadResult(
            media=[MediaItem(file_path=video_path, type="video")],
            title=info.get('title', 'unknown'),
            description=info.get('description', ''),
            author=info.get('uploader', 'unknown'),
        )

    def download_audio(self, url):
        info = json.loads(self.get_info_ytdlp(url))
        duration = info.get("duration", 0)
        if duration > self.max_duration:
            raise ValueError(
                f"[YouTubeDownloaderAudio] audio exceeds {self.max_duration}s"
            )

        result = super().download_audio(url)
        result.title = info.get("title", "")
        return result
