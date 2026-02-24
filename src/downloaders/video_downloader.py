import os
import tempfile
import yt_dlp
import subprocess
import shutil
import traceback
from yt_dlp.utils import DownloadError
from utils.logger import error


class VideoDownloader:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_path = os.path.join(self.temp_dir, "video_original.mp4")
        self.compressed_path = os.path.join(self.temp_dir, "video_compressed.mp4")
        self.IMPERSONATE_BROWSER = "Firefox-135"

    async def download_video(self, url):
        self.reset_temp_dir()
        ydl_opts = {
            'format': 'bv*+ba/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(self.temp_dir, "video_original.%(ext)s"),
            'noplaylist': True,
            'quiet': False,
            'no_warnings': True,
            'extract_flat': True,
            'restrictfilenames': True,
            'overwrites': True,
            'continuedl': False,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
                }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except DownloadError as e:
                error(f"[VideoDownloader] Error download media: {e}\n{traceback.format_exc()}")
                raise RuntimeError("[VideoDownloader] download failed") from e

        if not os.path.exists(self.original_path):
            
            raise FileNotFoundError("File non trovato dopo il download.")

        size_mb = os.path.getsize(self.original_path) / (1024 * 1024)
        final_path = self.original_path

        if size_mb > 50:
            self.compress_video(self.original_path, self.compressed_path)
            final_path = self.compressed_path

        return {
            "media": [{"file_path": final_path, "type": "video"}],
            "title": "",
            "description": "",
            "author": "",
        }


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

        #subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(command, check=True)

    def cleanup(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = None

    def reset_temp_dir(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_path = os.path.join(self.temp_dir, "video_original.mp4")
        self.compressed_path = os.path.join(self.temp_dir, "video_compressed.mp4")

    def get_size_video(self):
        return os.path.getsize(self.original_path) / (1024 * 1024)
