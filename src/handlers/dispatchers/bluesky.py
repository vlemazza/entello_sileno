from downloaders.bluesky_downloader import BlueSkyVideoDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_bluesky_caption
from services.logger import debug


class BlueskyDispatcher(BaseDispatcher):
    service_name = "Bluesky"

    def create_downloader(self):
        return BlueSkyVideoDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)
        content = result.content
        user = result.user

        debug("[Bluesky] post metadata fetched")

        if result.has_media:
            media_result = await downloader.fetch_media(url)
            media_list = media_result.media

            debug("[Bluesky] media downloaded")
        else:
            media_list = []
            debug("[Bluesky] no media just text")

        caption = build_bluesky_caption(content, user, url)

        await self.send_message(sender, media_list, caption)


_DISPATCHER = BlueskyDispatcher()


async def handle_bluesky(update, context, url):
    return await _DISPATCHER.run(update, context, url)
