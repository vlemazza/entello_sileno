import os
import subprocess
from pathlib import Path
from gallery_dl import config
from gallery_dl.extractor import find
from gallery_dl.job import DownloadJob
from downloaders.video_downloader import VideoDownloader



class TwitterDownloader(VideoDownloader):

    IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
    VIDEO_EXT = {".mp4", ".webm"}

    def __init__(self):
        super().__init__()
    

    async def download_tweet_post(self, url):
        extractor = find(url)
        extractor.initialize()


        items = list(extractor.items())

        try:
            data = items[0][2]
            content = data['content']
            user = data['author']['nick']
            media = True
        except Exception:
            user = extractor.user.title()
            content = await self.search_metadata(list(extractor.tweets()), 'full_text')
            media = False


        return {
            "content":content,
            "user": user,
            "media": media
        }

    async def download_tweet_media(self, url):
        self.reset_temp_dir()
        media_files = []

        config.set(("extractor", "twitter"), "directory", "")
        config.set(("extractor", "twitter"), "base-directory", self.temp_dir)

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

                size_mb = os.path.getsize(path) / (1024 * 1024)

                if size_mb > 50:
                    command = [
                        "nice", "-n", "19",
                        "ffmpeg",
                        "-i", str(path),
                        "-vf", "scale=-2:720",
                        "-c:v", "libx264",
                        "-crf", "35",
                        "-preset", "veryfast",
                        "-profile:v", "main",
                        "-c:a", "aac",
                        "-b:a", "128k",
                        "-y",
                        os.path.join(self.temp_dir, "video_compressed.mp4")
                    ]
                    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    path = os.path.join(self.temp_dir, "video_compressed.mp4")

            else:
                continue

            media_files.append({
                "file_path": str(path),
                "type": media_type,
            })

        return {
            "media": media_files,
            "title": "",
            "description": "",
            "author": "",
        }

    async def search_metadata(self, data, search):
        if isinstance(data, dict):
            for k, v in data.items():
                if k == search:
                    return v
                res = await self.search_metadata(v, search)
                if res is not None:
                    return res
        elif isinstance(data, list):
            for item in data:
                res = await self.search_metadata(item, search)
                if res is not None:
                    return res
        return None
