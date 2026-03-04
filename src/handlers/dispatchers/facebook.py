from downloaders.facebook_downloader import FacebookDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_facebook_caption
from services.logger import debug


class FacebookDispatcher(BaseDispatcher):
    service_name = "Facebook"

    def create_downloader(self):
        return FacebookDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)
        media_list = result.media
        title = result.title
        description = result.description
        author = result.author

        debug("[Facebook] media downloaded")

        caption = build_facebook_caption(title, description, author, url)
        
        await self.send_message(sender, media_list, caption)


_DISPATCHER = FacebookDispatcher()


async def handle_facebook(update, context, url):
    return await _DISPATCHER.run(update, context, url)
