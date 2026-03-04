import os
from pathlib import Path
from gallery_dl import config
from gallery_dl.extractor import find
from gallery_dl.job import DownloadJob
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem



class BlueSkyVideoDownloader(MediaDownloader):

    IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
    VIDEO_EXT = {".mp4", ".webm"}

    def __init__(self):
        super().__init__()


    async def fetch_post(self, url):
        extractor = find(url)
        extractor.initialize()


        items = list(extractor.items())
        
        content = ""
        user = "Unknown"
        media = False

        if items:

            data = items[0][2]
            content = data.get('content', data.get('text', ''))
            author_data = data.get('author', {})
            user = author_data.get('handle', author_data.get('displayName', "Unknown"))

            has_file_embed = 'embed' in data
            has_file_downloadable = any(item[0] == 3 for item in items)

            if (has_file_embed or has_file_downloadable):
                media = True
            else:
                media = False

        return DownloadResult(
            content=content,
            user=user,
            has_media=media,
        )

    async def fetch_media(self, url):
        self.reset_temp_dir()
        media_files = []

        config.set(("extractor", "bluesky"), "directory", "")
        config.set(("extractor", "bluesky"), "base-directory", self.temp_dir)

        extractor = find(url)
        extractor.initialize()


        job = DownloadJob(url)
        job.run() 

        for path in sorted(Path(self.temp_dir).rglob("*"), key=lambda item: str(item)):
            if not path.is_file():
                continue

            ext = path.suffix.lower()

            if ext in self.IMAGE_EXT:
                media_type = "image"
            elif ext in self.VIDEO_EXT:
                media_type = "video"
                path = self.finalize_video(str(path))

            else:
                continue

            media_files.append({
                "file_path": str(path),
                "type": media_type,
            })

        return DownloadResult(
            media=[MediaItem(file_path=m["file_path"], type=m["type"]) for m in media_files]
        )
