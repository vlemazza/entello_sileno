import os
import shutil
import subprocess
import json
import tempfile
import asyncio
from pathlib import Path
import aiohttp
from gallery_dl import config
from gallery_dl.extractor import find
from gallery_dl.job import DownloadJob
from services.logger import error, debug
from models.download_result import DownloadResult, MediaItem


class MediaDownloader:
    MAX_VIDEO_MB = 50
    IMPERSONATE_BROWSER = "Firefox-135"
    IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
    VIDEO_EXT = {".mp4", ".webm"}

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

    async def compress_video(self, input_file, output_file):
        command = [
            "nice", "-n", "19",
            "ffmpeg",
            "-i", str(input_file),
            "-vf", "scale=-2:720",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-qp", "35",
            "-preset", "fast",
            "-level", "4.2",
            "-profile:v", "main",
            "-c:a", "aac",
            "-b:a", "128k",
            "-y",
            str(output_file)
        ]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"[MediaDownloader] ffmpeg compress failed: {stderr.decode()}")

    async def extract_audio(self, input_file, output_file):
        command = [
            "nice", "-n", "19",
            "ffmpeg",
            "-i", str(input_file),
            "-vn",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-y",
            str(output_file),
        ]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"[MediaDownloader] ffmpeg extract failed: {stderr.decode()} MB")

    async def finalize_video(self, input_file, max_mb=None):
        threshold = max_mb or self.MAX_VIDEO_MB
        size_mb = self._get_size_mb(input_file)
        if size_mb <= threshold:
            return str(input_file)

        debug(f"[MediaDownloader] compressing video: {size_mb}")

        await self.compress_video(input_file, self.compressed_path)
        return str(self.compressed_path)

    def set_cookies_from_env(self, env_var, label):
        cookies_file = os.getenv(env_var)
        if not cookies_file or not os.path.exists(cookies_file):
            raise ValueError(f"File cookie non impostato per {label}")
        self.cookies_file = cookies_file

    async def _get_info_ytdlp(self, url, cookies_file=None):
        cmd = ["yt-dlp", "--dump-single-json"]
        cookies = self.cookies_file if cookies_file is None else cookies_file

        if cookies:
            cmd.extend(["--cookies", cookies])

        cmd.append(url)

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error(f"[MediaDownloader] Error dump info: {stderr.decode()}")
            raise RuntimeError("[MediaDownloader] dump info failed")
        return stdout.decode()

    async def get_info_from_ytdlp(self, url, cookies_file=None):
        return json.loads(await self._get_info_ytdlp(url, cookies_file=cookies_file))

    async def download_video(self, url, cookies_file=None, impersonate=False):
        self.reset_temp_dir()
        output_template = os.path.join(self.temp_dir, "video_original.%(ext)s")
        default_args = [
            "-f", "bv*+ba/best",
            "--merge-output-format", "mp4",
            "--no-playlist",
            "--recode-video=mp4",
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
            raise FileNotFoundError("File downlaoded not found.")

        final_path = await self.finalize_video(self.original_path)
        return final_path

    async def download_audio(self, url, cookies_file=None, impersonate=False):
        self.reset_temp_dir()

        info = await self.get_info_from_ytdlp(url, cookies_file=cookies_file)
        title = info.get("title", "")

        output_path = os.path.join(self.temp_dir, f"{title}.%(ext)s")

        cmd = [
            "yt-dlp",
            "-o", output_path,
            "--extract-audio",
            "--audio-format", "mp3",
        ]
        cookies = self.cookies_file if cookies_file is None else cookies_file
        if cookies:
            cmd.extend(["--cookies", cookies])

        if impersonate:
            cmd.extend(["--impersonate", self.IMPERSONATE_BROWSER])

        cmd.append(url)

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            _, stderr = await asyncio.wait_for(process.communicate(), timeout=300)

        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise TimeoutError("[MediaDownloader] Timeout durante il download")

        if process.returncode != 0:
            raise RuntimeError(f"[MediaDownloader] Error download audio: {stderr.decode()}")

        final_path = os.path.join(self.temp_dir, f"{title}.mp3")

        if not os.path.exists(final_path):
            raise FileNotFoundError("File not found.")

        return DownloadResult(media=[MediaItem(file_path=final_path, type="audio")])

    async def _download_file(self, url, path, headers=None):
        req_headers = headers or self.headers
        async with aiohttp.ClientSession(headers=req_headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.read()
        await asyncio.to_thread(Path(path).write_bytes, data)

    async def gallery_dl_download_media(
        self,
        url,
        extractor_key,
    ):
        self.reset_temp_dir()

        config.set(("extractor", extractor_key), "directory", "")
        config.set(("extractor", extractor_key), "base-directory", self.temp_dir)
        if self.cookies_file:
            config.set(("extractor", extractor_key), "cookies", self.cookies_file)

        extractor = find(url)
        extractor.initialize()

        job = DownloadJob(url)
        await asyncio.to_thread(job.run)

        media_files = []
        for path in sorted(Path(self.temp_dir).rglob("*"), key=lambda item: str(item)):
            if not path.is_file():
                continue

            ext = path.suffix.lower()
            if ext in self.IMAGE_EXT:
                media_type = "image"
            elif ext in self.VIDEO_EXT:
                media_type = "video"
                path = await self.finalize_video(str(path))
            else:
                continue

            media_files.append({
                "file_path": str(path),
                "type": media_type,
            })

        return DownloadResult(
            media=[MediaItem(file_path=m["file_path"], type=m["type"]) for m in media_files]
        )
