import os
import subprocess
import json
from downloaders.video_downloader import VideoDownloader
from pathlib import Path

class TikTokDownloader(VideoDownloader):
    def __init__(self):
        super().__init__()
        self.cookies_file = os.getenv("TK_COOKIES_FILE")
        if not self.cookies_file or not os.path.exists(self.cookies_file):
            raise ValueError("File cookie non impostato")
        self.user_agent = "sesso frank?"

    def download_video(self, url):

        self.reset_temp_dir()
        output_path = os.path.join(self.temp_dir, "video.mp4")

        cmd = [
            "yt-dlp",
            "--user-agent", self.user_agent,
            "--cookies", self.cookies_file,
            "-o", output_path,
            url
        ]

        info_cmd = [
            "yt-dlp",
            "--dump-single-json",
            "--user-agent", self.user_agent,
            "--cookies", self.cookies_file,
            url
        ]
        result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        try:
            subprocess.run(cmd, check=True, timeout=300)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"[TikTokDownloader] Errore download video: {e}")
        except subprocess.TimeoutExpired:
            raise TimeoutError("[TikTokDownloader] Timeout durante il download")

        if not os.path.exists(output_path):
            raise FileNotFoundError("File non trovato dopo il download.")

        return {
            "media": [{"file_path": output_path, "type": "video"}],
            "title": data.get("title") or "TikTok Video",
            "description": data.get("description") or "",
            "author": (data.get("uploader") or "").strip()
        }

    def download_photos(self, url):
            self.reset_temp_dir()
            media_files = []

            
            cmd = [
                "gallery-dl",
                "--cookies", self.cookies_file,
                "-d", self.temp_dir,
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

            return {
                "media": media_files,
                "title": "",
                "description": "",
                "author": ""
            }
