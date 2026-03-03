import os
import shutil
import subprocess
import tempfile
import asyncio
from pathlib import Path
from utils.logger import error
from models.download_result import DownloadResult, MediaItem


class MediaDownloader:
    MAX_VIDEO_MB = 50
    IMPERSONATE_BROWSER = "Firefox-135"

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_path = os.path.join(self.temp_dir, "video_original.mp4")
        self.compressed_path = os.path.join(self.temp_dir, "video_compressed.mp4")
        self.headers = {"User-Agent": "Sesso Frank?"}
        self.cookies_file = None

    def reset_temp_dir(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_path = os.path.join(self.temp_dir, "video_original.mp4")
        self.compressed_path = os.path.join(self.temp_dir, "video_compressed.mp4")

    def cleanup(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = None

    def _get_size_mb(self, path):
        return os.path.getsize(path) / (1024 * 1024)

    def compress_video(self, input_file, output_file):
        command = [
            "nice", "-n", "19",
            "ffmpeg",
            "-i", str(input_file),
            "-vf", "scale=-2:720",
            "-c:v", "libx264",
            "-qp", "35",
            "-preset", "fast",
            "-level", "4.2",
            "-profile:v", "main",
            "-c:a", "aac",
            "-b:a", "128k",
            "-y",
            str(output_file)
        ]
        subprocess.run(command, check=True)

    def finalize_video(self, input_file, max_mb=None):
        threshold = max_mb or self.MAX_VIDEO_MB
        size_mb = self._get_size_mb(input_file)
        if size_mb <= threshold:
            return str(input_file)

        self.compress_video(input_file, self.compressed_path)
        return str(self.compressed_path)

    def set_cookies_from_env(self, env_var, label):
        cookies_file = os.getenv(env_var)
        if not cookies_file or not os.path.exists(cookies_file):
            raise ValueError(f"File cookie non impostato per {label}")
        self.cookies_file = cookies_file

    def get_info_ytdlp(self, url, cookies_file=None):
        cmd = ["yt-dlp", "--dump-single-json"]
        cookies = self.cookies_file if cookies_file is None else cookies_file

        if cookies:
            cmd.extend(["--cookies", cookies])

        cmd.append(url)

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout

    async def download_video(self, url, cookies_file=None, impersonate=False):
        self.reset_temp_dir()
        output_template = os.path.join(self.temp_dir, "video_original.%(ext)s")
        default_args = [
            "-f", "bv*+ba/best",
            "--merge-output-format", "mp4",
            "--no-playlist",
            "--no-warnings",
            "--restrict-filenames",
            "--force-overwrites",
            "--no-continue",
        ]
        cmd = ["yt-dlp", "-o", output_template]

        cookies = self.cookies_file if cookies_file is None else cookies_file

        if cookies:
            cmd.extend(["--cookies", cookies])

        if impersonate:
            cmd.extend(["--impersonate", self.IMPERSONATE_BROWSER])
        
        cmd.extend(default_args)
        cmd.append(url)

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()
        if process.returncode != 0:
            error(f"[MediaDownloader] Error download media: {stderr.decode()}")
            raise RuntimeError("[MediaDownloader] download failed")

        if not os.path.exists(self.original_path):
            raise FileNotFoundError("File non trovato dopo il download.")

        final_path = self.finalize_video(self.original_path)
        return final_path

    def download_audio(self, url, cookies_file=None):
        self.reset_temp_dir()
        output_path = os.path.join(self.temp_dir, "audio.%(ext)s")
        cmd = [
            "yt-dlp",
            "-o", output_path,
            "--extract-audio",
            "--audio-format", "mp3",
        ]
        cookies = self.cookies_file if cookies_file is None else cookies_file
        if cookies:
            cmd.extend(["--cookies", cookies])
        cmd.append(url)

        try:
            subprocess.run(cmd, check=True, timeout=300)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"[MediaDownloader] Errore download audio: {e}")
        except subprocess.TimeoutExpired:
            raise TimeoutError("[MediaDownloader] Timeout durante il download")

        final_path = os.path.join(self.temp_dir, "audio.mp3")
        if not os.path.exists(final_path):
            raise FileNotFoundError("File non trovato dopo il download.")

        return DownloadResult(media=[MediaItem(file_path=final_path, type="audio")])
