from downloaders.twitter_downloader import TwitterDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_twitter_caption
from utils.logger import debug


class TwitterDispatcher(BaseDispatcher):
    service_name = "Twitter"

    def create_downloader(self):
        return TwitterDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)
        content = result.content
        user = result.user

        debug("[Twitter] post metadata scaricato")

        if result.has_media:
            media_result = await downloader.fetch_media(url)
            media_list = media_result.media

            debug("[Twitter] media scaricato")
        else:
            media_list = []
            debug("[Twitter] no media solo testo")

        caption = build_twitter_caption(content, user, url)

        await self.send_message(sender, media_list, caption)


_DISPATCHER = TwitterDispatcher()


async def handle_twitter(update, context, url):
    return await _DISPATCHER.run(update, context, url)
