from downloaders.hackernews_downloader import HackerNewsDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_hn_caption


class HackerNewsDispatcher(BaseDispatcher):
    service_name = "HackerNews"

    def create_downloader(self):
        return HackerNewsDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)
        caption = build_hn_caption(
            result.title,
            result.user,
            result.external_url,
            result.content,
            url,
        )
        await self.send_message(sender, [], caption)


_DISPATCHER = HackerNewsDispatcher()


async def handle_hackernews(update, context, url):
    return await _DISPATCHER.run(update, context, url)
