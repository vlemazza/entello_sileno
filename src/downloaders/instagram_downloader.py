import os
import re
from pathlib import Path
import json
import subprocess
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem


class InstagramDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()
        self.set_cookies_from_env("IG_COOKIES_FILE", "Instagram")

        self.instaloader_session = os.getenv("IG_SESSION_FILE")

        if not self.instaloader_session or not os.path.exists(self.instaloader_session):
            raise ValueError("Instaloader session not found")

    async def fetch_video_post(self, url):
        video_path = await self.download_video(url)
        data = json.loads(self.get_info_ytdlp(url))
        return DownloadResult(
            media=[MediaItem(file_path=video_path, type="video")],
            title=data.get("title") or "Instagram Video",
            description=data.get("description") or "",
            author=(data.get("uploader") or "").strip(),
        )

    async def fetch_image_post(self, url):
        self.reset_temp_dir()
        media_files = []

        match = re.search(r"/p/([^/]+)/?", url)
        if not match:
            raise ValueError("Cannot extract shortcode Instagram")

        shortcode = match.group(1)

        cmd = [
            "/usr/local/bin/instaloader",
            "--sessionfile", self.instaloader_session,
            "--no-video-thumbnails",
            "--filename-pattern=a",
            "--no-videos",
            "--",
            f"-{shortcode}",
        ]
        

        subprocess.run(
            cmd,
            cwd=self.temp_dir,
            timeout=120
        )

        save_dir = os.path.join(self.temp_dir, f"-{shortcode}")

        caption = ""
        uploader = ""

        for file in Path(save_dir).rglob("*"):
            if file.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                media_files.append({
                    "file_path": str(file),
                    "type": "image",
                })

            elif file.name.endswith(".txt"):
                with open(file, "r", encoding="utf-8") as f:
                    caption = f.read().strip()

            elif file.name.endswith(".json"):
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        uploader = data.get("owner_username", "")
                except Exception:
                    pass

        media_files.sort(key=lambda item: self._extract_media_index(item["file_path"]))

        if not media_files:
            raise RuntimeError("Image not found")


        
        return DownloadResult(
            media=[MediaItem(file_path=m["file_path"], type=m["type"]) for m in media_files],
            title=caption if caption else "Instagram Post",
            description=caption,
            author=uploader.strip(),
        )

    def _extract_media_index(self, path_str):
        match = re.search(r"_(\d+)\.[^.]+$", path_str)
        return int(match.group(1)) if match else -1
