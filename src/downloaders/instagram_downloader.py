import os
import re
from pathlib import Path
import json
import asyncio
import subprocess
from downloaders.video_downloader import VideoDownloader
from urllib.parse import urlparse, urlunparse

class InstagramDownloader(VideoDownloader):
    def __init__(self):
        super().__init__()
        self.cookies_file = os.getenv("IG_COOKIES_FILE")
        if not self.cookies_file or not os.path.exists(self.cookies_file):
            raise ValueError("File cookie non impostato")

        self.instaloader_session = os.getenv("IG_SESSION_FILE")
        if not self.instaloader_session or not os.path.exists(self.instaloader_session):
            raise ValueError("Sessione Instaloader non trovata")

    async def download_post(self, url):

        parsed = urlparse(url)
        url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

        if "/p/" in parsed.path:
            try:
                return await self.download_image_post(url)
            except Exception:
                return await self.download_video_post(url)

        elif "/reel/" in parsed.path:
            return await self.download_video_post(url)
        else:
            raise ValueError("URL Instagram non supportato. Deve contenere /p/ o /reel/")

    async def download_video_post(self, url):
        self.reset_temp_dir()
        media_files = []

        output_template = os.path.join(self.temp_dir, "video_original_%(playlist_index)s.%(ext)s")
            
        cmd = [
            "yt-dlp",
            "--no-playlist",
            "--cookies", self.cookies_file,
            "-f", "bv*+ba/best",
            "-o", output_template,
            "--postprocessor-args",
            "-c:v libx264 -profile:v main -level 4.1 -pix_fmt yuv420p -preset veryfast -crf 28 -c:a aac -b:a 128k -movflags +faststart",
            url
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(stderr.decode())

        for f in sorted(os.listdir(self.temp_dir)):
            path = os.path.join(self.temp_dir, f)
            ext = os.path.splitext(f)[1][1:].lower()

            if not media_files:
                final_name = os.path.join(self.temp_dir, "video_original.mp4")
                os.rename(path, final_name)
                path = final_name

                if self.get_size_video() > 50:
                    self.compress_video(path, self.compressed_path)
                    path = self.compressed_path

            if ext in {"mp4", "mkv", "webm"}:
                media_files.append({
                    "file_path": path,
                    "type": "video",
                })

        info_cmd = [
            "yt-dlp",
            "--dump-single-json",
            "--cookies", self.cookies_file,
            url
        ]
        result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        return {
            "media": media_files,
            "title": data.get("title") or "Instagram Video",
            "description": data.get("description") or "",
            "author": (data.get("uploader") or "").strip()
        }

    async def download_image_post(self, url):
        self.reset_temp_dir()
        media_files = []

        match = re.search(r"/p/([^/]+)/?", url)
        if not match:
            raise ValueError("Impossibile estrarre shortcode Instagram")

        shortcode = match.group(1)

        cmd = [
            "/usr/local/bin/instaloader",
            "--sessionfile", self.instaloader_session,
            "--no-video-thumbnails",
            "--no-videos",
            "--",
            f"-{shortcode}",
        ]
        

        subprocess.run(
            cmd,
            check=True,
            cwd=self.temp_dir,
            timeout=120
        )

        post_dir = os.path.join(self.temp_dir, f"-{shortcode}")

        caption = ""
        uploader = ""

        for file in sorted(Path(post_dir).rglob("*"), key=lambda item: str(item)):
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

        if not media_files:
            raise RuntimeError("Nessuna immagine trovata")


        
        return {
            "media": media_files,
            "title": caption[:100] if caption else "Instagram Post",
            "description": caption,
            "author": uploader.strip()
        }
