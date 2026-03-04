import os
import requests
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem
from services.logger import debug
from pathlib import Path
from RedDownloader import RedDownloader


class RedditDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()

    async def fetch_post(self, url):

        self.reset_temp_dir()
        media_files = []

        json_url = url + "/.json"

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

        return DownloadResult(
            media=[MediaItem(file_path=m["file_path"], type=m["type"]) for m in media_files],
            title=title,
            external_url=external_url,
            description=selftext,
            author=f"u/{author}",
            subreddit=f"r/{subreddit}",
        )


    async def _download_video(self, url, media_files):

        video_path = await self.download_video(url)
        media_files.append({
            "file_path": video_path,
            "type": "video",
        })


    async def _download_image(self, url, media_files):  
        RedDownloader.Download(url , destination=self.temp_dir)    
        for path_obj in Path(self.temp_dir).rglob("*"):
            if path_obj.is_file():
                media_files.append({
                    "file_path": str(path_obj),
                    "type": "image",
                })     
