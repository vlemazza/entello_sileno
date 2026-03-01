import os
import requests
from downloaders.video_downloader import VideoDownloader
from utils.logger import debug
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

    async def download_post(self, url):

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
            await self._download_image(url, media_files)

        elif post_data.get("is_video"):
            video_url = (
                post_data.get("media", {})
                .get("reddit_video", {})
                .get("dash_url")
            )

            if video_url:
                await self._download_video(video_url, media_files)
            

        elif post_data.get("post_hint") == "image":
            await self._download_image(url, media_files)

        return {
            "media": media_files,
            "title": title,
            "external_url": external_url,
            "description": selftext,
            "author": f"u/{author}",
            "subreddit": f"r/{subreddit}",
        }

    async def _download_video(self, url, media_files):

        result = await self.download_video(url)

        media_files.append({
            "file_path": result["media"][0]["file_path"],
            "type": "video",
        })


    async def _download_image(self, url, media_files):

        
        for path_obj in sorted(Path(self.temp_dir).rglob("*"), key=lambda item: str(item)):
            if path_obj.is_file():
                media_files.append({
                    "file_path": str(path_obj),
                    "type": "image",
                })     
