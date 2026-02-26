import os
import requests
from downloaders.video_downloader import VideoDownloader
from utils.logger import debug
from RedDownloader import RedDownloader
from pathlib import Path


class RedditDownloader(VideoDownloader):
    def __init__(self):
        super().__init__()
        self.headers  = {
            "User-Agent": "Mozilla/5.0 (GNU/HURD)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
        }

    def download_post(self, url):

        self.reset_temp_dir()
        media_files = []

        json_url = url + "/.json"

        print(json_url)

        r = requests.get(json_url, headers=self.headers)
        r.raise_for_status()
        data = r.json()

        post_data = data[0]["data"]["children"][0]["data"]

        title = post_data.get("title", "")
        selftext = post_data.get("selftext", "")
        subreddit = post_data.get("subreddit", "")
        author = post_data.get("author", "")
        external_url = post_data.get("url_overridden_by_dest", "")

        if post_data.get("is_gallery"):
            self._download_image(url, media_files)

        elif post_data.get("is_video"):
            video_url = (
                post_data.get("media", {})
                .get("reddit_video", {})
                .get("fallback_url")
            )

            if video_url:
                file_path = self._download_video(video_url)
                media_files.append({
                    "file_path": file_path,
                    "type": "video",
                })

        elif post_data.get("post_hint") == "image":
            self._download_image(url, media_files)

        return {
            "media": media_files,
            "title": title,
            "external_url": external_url,
            "description": selftext,
            "author": f"u/{author}",
            "subreddit": f"r/{subreddit}",
        }

    def _download_video(self, url):
        local_filename = os.path.join(self.temp_dir, url.split("/")[-1].split("?")[0])

        r = requests.get(url, headers=self.headers)
        r.raise_for_status()

        with open(local_filename, "wb") as f:
            f.write(r.content)

        return local_filename

    def _download_image(self, url, media_files):

        post = RedDownloader.Download(
                url,
                destination=os.path.join(self.temp_dir, "")
            )

        for path_obj in sorted(Path(self.temp_dir).rglob("*"), key=lambda item: str(item)):
            if path_obj.is_file():
                media_files.append({
                    "file_path": str(path_obj),
                    "type": "image",
                })     
