import aiohttp
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult
from utils.urls import get_hn_item_id


class HackerNewsDownloader(MediaDownloader):
    HN_API_BASE = "https://hacker-news.firebaseio.com/v0"

    def __init__(self):
        super().__init__()

    async def fetch_post(self, url):
        item_id = await get_hn_item_id(url)
        api_url = f"{self.HN_API_BASE}/item/{item_id}.json"

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                data = await response.json()

        title = data.get("title", "")
        content = data.get("text", "") or ""
        user = data.get("by", "")
        external_url = data.get("url", "")

        return DownloadResult(
            media=[],
            title=title,
            content=content,
            user=user,
            external_url=external_url,
            has_media=False,
        )
