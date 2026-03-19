import asyncio
from gallery_dl import config
from gallery_dl.extractor import find
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem



class TwitterDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()

    async def fetch_post(self, url):
        config.set(("extractor", "twitter"), "text-tweets", True)
        config.set(("postprocessor",), "metadata", True)
        config.set(("metadata",), "event", "post")
        config.set(("metadata",), "filename", "{tweet_id}")

        extractor = find(url)
        extractor.initialize()


        items = await asyncio.to_thread(lambda: list(extractor.items()))

        data = items[0][2]
        content = data.get("content") or data.get("full_text") or data.get("text") or ""
        author_data = data.get("author") or {}
        user = (
            author_data.get("nick")
            or author_data.get("name")
            or author_data.get("username")
            or "Unknown"
        )
        media = True

        return DownloadResult(
            content=content,
            user=user,
            has_media=media,
        )


    async def fetch_media(self, url):
        return await self.gallery_dl_download_media(
            url,
            "twitter",
        )
