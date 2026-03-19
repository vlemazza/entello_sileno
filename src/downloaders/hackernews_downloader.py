import aiohttp
import re
from html import unescape
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
        content = self._clean_hn_text(data.get("text", "") or "")
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

    def _clean_hn_text(self, text):
        if not text:
            return ""
        value = unescape(text)
        value = re.sub(r"<\s*p\s*/?>", "\n", value, flags=re.IGNORECASE)
        value = re.sub(r"<\s*/\s*p\s*>", "\n", value, flags=re.IGNORECASE)
        value = re.sub(
            r'<\s*a\s+[^>]*href="([^"]+)"[^>]*>.*?<\s*/\s*a\s*>',
            r"\1",
            value,
            flags=re.IGNORECASE | re.DOTALL,
        )
        value = re.sub(r"<[^>]+>", "", value)
        return value.strip()
