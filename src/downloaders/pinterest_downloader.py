import asyncio
from gallery_dl.extractor import find
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult


class PinterestDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()

    async def fetch_post(self, url):
        extractor = find(url)
        extractor.initialize()
        items = await asyncio.to_thread(lambda: list(extractor.items()))

        data = items[0][2]

        title = data.get("title") or data.get("seo_title") or ""
        content = data.get("description") or ""

        pinner = data.get("pinner") or {}
        user = pinner.get("username") or ""
        

        return DownloadResult(
            content=content,
            title=title,
            user=user,
            has_media=True,
        )

    async def fetch_media(self, url):
        return await self.gallery_dl_download_media(url, "pinterest")
