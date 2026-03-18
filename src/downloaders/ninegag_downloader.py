import os
import asyncio
import aiohttp
from pathlib import Path
from utils.urls import get_9gag_api_url
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem



class NineGagDownloader(MediaDownloader):

    def __init__(self):
        super().__init__()

    async def _download_file(self, url, path):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.read()
        await asyncio.to_thread(Path(path).write_bytes, data)


    async def fetch_post(self, url):
        api_url = await get_9gag_api_url(url)
        data = await self._fetch_json(api_url)

        post = data.get("data", {}).get("post", {})

        title = post.get("title", "")
        content = post.get("description", "")
        post_type = post.get("type", "")
        user = post.get("creator", {}).get("username", "")

        if post_type == "Photo":
            self.reset_temp_dir()
            image_path = os.path.join(self.temp_dir, "image_source.jpg")
            images = post.get("images", {})
            image_url = images.get("image700", {}).get("url")

            if not image_url:
                raise RuntimeError("9GAG image URL not found in post json")
                
            await self._download_file(image_url, image_path)

            return DownloadResult(
            media=[MediaItem(file_path=image_path, type="image")],
            title=title,
            content=content,
            user=user.strip(),
            )
        else:
            video_path = await self.download_video(url)
            return DownloadResult(
            media=[MediaItem(file_path=video_path, type="video")],
            title=title,
            content=content,
            user=user,
            )

    async def _fetch_json(self, url):
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    response.raise_for_status() 
                    data = await response.json(content_type=None)
            return data
        except Exception as e:
            raise RuntimeError(f"Error fetch json: {e}")
