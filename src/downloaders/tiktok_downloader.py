import os
import json
import asyncio
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem
from pathlib import Path

class TikTokDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()
        self.set_cookies_from_env("TK_COOKIES_FILE", "TikTok")

    """
     async def download_video(self, url):

        data = await self.get_info_from_ytdlp(url)
        output_path = await super().download_video(url)
        if not os.path.exists(output_path):
            raise FileNotFoundError("File not found.")

        return DownloadResult(
            media=[MediaItem(file_path=output_path, type="video")],
            title=data.get("title") or "TikTok Video",
            content=data.get("description") or "",
            user=(data.get("uploader") or "").strip(),
        )
    """

    async def fetch_post(self, url):
            self.reset_temp_dir()
            cmd = [
                "gallery-dl",
                "--cookies", self.cookies_file,
                "--no-download",
                "-d", self.temp_dir,
                "--write-info-json",
                url
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            _, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"gallery-dl failed: {stderr.decode()}")

            for path_obj in Path(self.temp_dir).rglob("*"):
                file_path = str(path_obj)
                file_name = file_path.lower()

                suffix = Path(file_name).suffix.lower()
                if suffix == ".json":
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

            return DownloadResult(
                title=data.get("title") or "",
                content=data.get("desc") or "",
                user=(data["author"]["nickname"] or "").strip(),
                has_media=True,
            )

    async def fetch_media(self, url):
        media_result = await self.gallery_dl_download_media(url, "tiktok")
        for path_obj in Path(self.temp_dir).rglob("*"):
            if not path_obj.is_file():
                continue
            if path_obj.suffix.lower() == ".mp3":
                media_result.media.append(MediaItem(file_path=str(path_obj), type="audio"))
        return media_result

    async def download_audio(self, url):
        data = await self.get_info_from_ytdlp(url)
        result = await super().download_audio(url)
        result.title = data.get("title") or "TikTok Audio"
        result.user = (data.get("uploader") or "").strip()
        return result
