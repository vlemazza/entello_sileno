import os
import json
import subprocess
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem
from pathlib import Path

class TikTokDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()
        self.set_cookies_from_env("TK_COOKIES_FILE", "TikTok")

    async def download_video(self, url):

        self.reset_temp_dir()
        data = json.loads(self.get_info_ytdlp(url))
        output_path = await super().download_video(url)
        if not os.path.exists(output_path):
            raise FileNotFoundError("File not found.")

        return DownloadResult(
            media=[MediaItem(file_path=output_path, type="video")],
            title=data.get("title") or "TikTok Video",
            content=data.get("description") or "",
            user=(data.get("uploader") or "").strip(),
        )

    def download_photos(self, url):
            self.reset_temp_dir()
            media_files = []
         
            cmd = [
                "gallery-dl",
                "--cookies", self.cookies_file,
                "-d", self.temp_dir,
                "--write-info-json",
                url
            ]
            subprocess.run(cmd, check=True)

            for path_obj in Path(self.temp_dir).rglob("*"):
                file_path = str(path_obj)
                file_name = file_path.lower()
                if file_name.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    media_files.append({"file_path": file_path, "type": "image"})
                elif file_name.endswith(".mp3"):
                    media_files.append({"file_path": file_path, "type": "audio"})
                elif file_name.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

            return DownloadResult(
                media=[MediaItem(file_path=m["file_path"], type=m["type"]) for m in media_files],
                content=data.get("desc") or "",
                user=(data["author"]["nickname"] or "").strip(),
            )

    async def download_audio(self, url):
        data = json.loads(self.get_info_ytdlp(url))
        result = await super().download_audio(url)
        result.title = data.get("title") or "TikTok Audio"
        result.user = (data.get("uploader") or "").strip()
        return result
