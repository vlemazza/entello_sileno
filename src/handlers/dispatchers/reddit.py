from downloaders.reddit_downloader import RedditDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_reddit_caption
from services.logger import debug


class RedditDispatcher(BaseDispatcher):
    service_name = "Reddit"

    def create_downloader(self):
        return RedditDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)

        media_list = result.media or []
        title = result.title or ""
        content = result.content or ""
        external_url = result.external_url or ""
        user = result.user or ""
        subreddit = result.subreddit or ""

        caption = build_reddit_caption(
            title,
            content,
            external_url,
            user,
            subreddit,
            url
        )

        await self.send_message(sender, media_list, caption)


class RedditAudioDispatcher(BaseDispatcher):
    service_name = "Reddit"

    def create_downloader(self):
        return RedditDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.download_audio(url)
        audio_path = result.first_media_path()
        await sender.send_audio(audio_path)


_DISPATCHER = RedditDispatcher()
_AUDIO_DISPATCHER = RedditAudioDispatcher()

async def handle_reddit(update, context, url):
    return await _DISPATCHER.run(update, context, url)

async def handle_reddit_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
