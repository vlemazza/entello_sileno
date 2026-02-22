import os
import subprocess
from pathlib import Path
from gallery_dl import config
from gallery_dl.extractor import find
from gallery_dl.job import DownloadJob
from downloaders.video_downloader import VideoDownloader
import json



class BlueSkyVideoDownloader(VideoDownloader):

    IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
    VIDEO_EXT = {".mp4", ".webm"}

    def __init__(self):
        super().__init__()


    async def download_bluesky_post(self, url):
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

        return {
            "content":content,
            "user": user,
            "media": media
        }


    async def download_bluesky_media(self, url):
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



