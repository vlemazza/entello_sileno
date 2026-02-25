import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from downloaders.video_downloader import VideoDownloader


class ThreadsDownloader(VideoDownloader):

    def __init__(self):
        super().__init__()

    def download_post(self, url):

        self.reset_temp_dir()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        media_files = []

        body_text_container = soup.find(class_="BodyTextContainer")
        caption = body_text_container.get_text(strip=True) if body_text_container else ""

        name_container = soup.find("div", class_="NameContainer")
        author = ""
        if name_container:
            span = name_container.find("span")
            if span:
                author = span.get_text(strip=True)

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

        return {
            "media": media_files,
            "description": caption,
            "author": author,
        }

    def _download_file(self, url, path):
        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(path, "wb") as f:
            f.write(r.content)