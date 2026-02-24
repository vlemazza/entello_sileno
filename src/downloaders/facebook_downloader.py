import os
import json
import asyncio
import subprocess
from downloaders.video_downloader import VideoDownloader

class FacebookDownloader(VideoDownloader):
    def __init__(self):
        super().__init__()
        self.cookies_file = os.getenv("FB_COOKIES_FILE")
        if not self.cookies_file or not os.path.exists(self.cookies_file):
            raise ValueError("File cookie non impostato per Facebook")

    async def download_post(self, url):
        self.reset_temp_dir()
        media_files = []

        output_template = os.path.join(self.temp_dir, "video_original.%(ext)s")
            
        cmd = [
            "yt-dlp",
            "--no-playlist",
            #"--cookies", self.cookies_file,
            "-f", "bv*+ba/best",
            "--impersonate", self.IMPERSONATE_BROWSER,
            "-o", output_template,
            url
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:
            try:
                return await self.download_image_post(url)
            except Exception as e:
                raise RuntimeError(f"Errore durante il download del video: {stderr.decode()} Prova immagine: {e}")


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
            #"--cookies", self.cookies_file,
            url
        ]
        result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        return {
            "media": media_files,
            "title": data.get("title") or "Facebook Video",
            "description": data.get("description") or "",
            "author": (data.get("uploader") or "").strip()
        }

    async def download_image_post(self, url):
        self.reset_temp_dir()
        media_files = []

        output_template = os.path.join(self.temp_dir, "media_%(autonumber)s.%(ext)s")

        cmd = [
            "yt-dlp",
            "--no-playlist",
            "--cookies", self.cookies_file,
            "-o", output_template,
            url
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        _, stderr = await process.communicate()

        for f in sorted(os.listdir(self.temp_dir)):
            path = os.path.join(self.temp_dir, f)
            ext = os.path.splitext(f)[1][1:].lower()

            if ext in {"jpg", "jpeg", "png", "webp"}:
                media_files.append({
                    "file_path": path,
                    "type": "image",
                })

        info_cmd = [
            "yt-dlp",
            "--dump-single-json",
            "--cookies", self.cookies_file,
            url
        ]
        result = subprocess.run(info_cmd, capture_output=True, text=True)
        data = {}
        if result.returncode == 0:
            data = json.loads(result.stdout)
        elif not media_files:
            raise RuntimeError(f"Failed to download from Facebook. yt-dlp stderr: {stderr.decode()}")

        description = data.get("description") or data.get("title") or ""

        return {
            "media": media_files,
            "title": data.get("title") or "Facebook Post",
            "description": description,
            "author": (data.get("uploader") or "").strip()
        }

