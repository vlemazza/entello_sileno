from downloaders.reddit_downloader import RedditDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_reddit_caption
from utils.logger import debug


class RedditDispatcher(BaseDispatcher):
    service_name = "Reddit"

    def create_downloader(self):
        return RedditDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)

        media_list = result.media or []
        title = result.title or ""
        description = result.description or ""
        external_url = result.external_url or ""
        author = result.author or ""
        subreddit = result.subreddit or ""

        caption = build_reddit_caption(
            title,
            description,
            external_url,
            author,
            subreddit,
            url
        )

        await self.send_message(sender, media_list, caption)

_DISPATCHER = RedditDispatcher()


async def handle_reddit(update, context, url):
    return await _DISPATCHER.run(update, context, url)
