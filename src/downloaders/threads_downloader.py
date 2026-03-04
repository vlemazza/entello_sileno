import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem
from models.user_feedback import UnsupportedMediaType


class ThreadsDownloader(MediaDownloader):

    def __init__(self):
        super().__init__()

    def fetch_post(self, url):

        self.reset_temp_dir()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        media_files = []

        body_text_container = soup.find(class_="BodyTextContainer")
        caption = body_text_container.get_text(strip=True) if body_text_container else ""

        name_container = soup.find("div", class_="NameContainer")
        user = ""
        if name_container:
            span = name_container.find("span")
            if span:
                user = span.get_text(strip=True)

        media_containers = soup.select(".MediaContainer, .SoloMediaContainer")

        counter = 1

        for container in media_containers:

            videos = container.find_all("video")
            for video in videos:
                source = video.find("source")
                if source and source.get("src"):
                    media_url = urljoin(url, source["src"])
                    ext = "mp4"

                    file_path = os.path.join(
                        self.temp_dir,
                        f"media_{counter}.{ext}"
                    )

                    self._download_file(media_url, file_path)

                    media_files.append({
                        "file_path": file_path,
                        "type": "video",
                    })

                    counter += 1

            images = container.find_all("img")
            for img in images:
                if img.get("src"):
                    media_url = urljoin(url, img["src"])
                    ext = media_url.split("?")[0].split(".")[-1]

                    file_path = os.path.join(
                        self.temp_dir,
                        f"media_{counter}.{ext}"
                    )

                    self._download_file(media_url, file_path)

                    media_files.append({
                        "file_path": file_path,
                        "type": "image",
                    })

                    counter += 1

        return DownloadResult(
            media=[MediaItem(file_path=m["file_path"], type=m["type"]) for m in media_files],
            content=caption,
            user=user,
        )

    async def download_audio(self, url):
        self.reset_temp_dir()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        media_containers = soup.select(".MediaContainer, .SoloMediaContainer")
        video_url = None

        for container in media_containers:
            video = container.find("video")
            if video:
                source = video.find("source")
                if source and source.get("src"):
                    video_url = urljoin(url, source["src"])
                    break

        if not video_url:
            raise UnsupportedMediaType("Audio not available for this Threads post.")

        audio_path = os.path.join(self.temp_dir, "audio.mp3")

        raw_path = os.path.join(self.temp_dir, "audio_source.mp4")
        self._download_file(video_url, raw_path)
        self.extract_audio(raw_path, audio_path)
        if os.path.exists(raw_path):
            os.remove(raw_path)

        if not os.path.exists(audio_path):
            raise RuntimeError("Audio file not found after conversion.")

        return DownloadResult(media=[MediaItem(file_path=audio_path, type="audio")])


    def _download_file(self, url, path):
        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(path, "wb") as f:
            f.write(r.content)
