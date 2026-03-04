from downloaders.threads_downloader import ThreadsDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_threads_caption
from services.logger import debug


class ThreadsDispatcher(BaseDispatcher):
    service_name = "Threads"

    def create_downloader(self):
        return ThreadsDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = downloader.fetch_post(url)

        content = result.content or ""
        user = result.user or ""
        media_list = result.media or []

        debug("[Threads] post metadata fetched")

        caption = build_threads_caption(content, user, url)

        await self.send_message(sender, media_list, caption)


_DISPATCHER = ThreadsDispatcher()


async def handle_threads(update, context, url):
    return await _DISPATCHER.run(update, context, url)
