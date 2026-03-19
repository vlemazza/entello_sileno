import os
import asyncio
from gallery_dl.extractor import find
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem



class BlueSkyDownloader(MediaDownloader):
    def __init__(self):
        super().__init__()


    async def fetch_post(self, url):
        extractor = find(url)
        extractor.initialize()


        items = await asyncio.to_thread(lambda: list(extractor.items()))
        
        data = items[0][2]
        content = data.get('content', data.get('text', ''))
        author_data = data.get('author', {})
        user = author_data.get('handle', author_data.get('displayName', "Unknown"))

        has_file_embed = 'embed' in data
        has_file_downloadable = any(item[0] == 3 for item in items)

        if (has_file_embed or has_file_downloadable):
            media = True
        else:
            media = False

        return DownloadResult(
            content=content,
            user=user,
            has_media=media,
        )

    async def fetch_media(self, url):
        return await self.gallery_dl_download_media(
            url,
            "bluesky",
        )
