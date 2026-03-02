from downloaders.instagram_downloader import InstagramDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_instagram_caption
from utils.logger import debug
from urllib.parse import urlparse, urlunparse


class InstagramDispatcher(BaseDispatcher):
    service_name = "Instagram"

    def create_downloader(self):
        return InstagramDownloader()

    async def process(self, update, context, url, downloader, sender):
        parsed = urlparse(url)
        normalized_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

        if "/p/" in parsed.path:
            try:
                result = await downloader.fetch_image_post(normalized_url)
            except Exception:
                result = await downloader.fetch_video_post(normalized_url)
        elif "/reel/" in parsed.path:
            result = await downloader.fetch_video_post(normalized_url)
        else:
            raise ValueError("URL Instagram not supported; /p/ o /reel/")

        media_list = result.media
        title = result.title
        description = result.description
        author = result.author

        debug("[Instagram] media downloaded")

        caption = build_instagram_caption(title, description, author, url)
        
        await self.send_message(sender, media_list, caption)


_DISPATCHER = InstagramDispatcher()


async def handle_instagram(update, context, url):
    return await _DISPATCHER.run(update, context, url)
