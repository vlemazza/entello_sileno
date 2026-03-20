from downloaders.pinterest_downloader import PinterestDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_pinterest_caption
from services.logger import debug


class PinterestDispatcher(BaseDispatcher):
    service_name = "Pinterest"

    def create_downloader(self):
        return PinterestDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)
        media_result = await downloader.fetch_media(url)
        media_list = media_result.media

        debug("[Pinterest] media downloaded")

        caption = build_pinterest_caption(result.title, result.content, result.user, url)
        await self.send_message(sender, media_list, caption)


_DISPATCHER = PinterestDispatcher()


async def handle_pinterest(update, context, url):
    return await _DISPATCHER.run(update, context, url)
