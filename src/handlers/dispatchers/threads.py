from downloaders.threads_downloader import ThreadsDownloader
from handlers.dispatchers.base import BaseDispatcher
from models.user_feedback import UnsupportedMediaType
from services.caption_builder import build_threads_caption
from services.logger import debug


class ThreadsDispatcher(BaseDispatcher):
    service_name = "Threads"

    def create_downloader(self):
        return ThreadsDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)

        content = result.content or ""
        user = result.user or ""
        media_list = result.media or []

        debug("[Threads] post metadata fetched")

        caption = build_threads_caption(content, user, url)

        await self.send_message(sender, media_list, caption)

class ThreadsAudioDispatcher(BaseDispatcher):
    service_name = "Threads"

    def create_downloader(self):
        return ThreadsDownloader()

    async def process(self, update, context, url, downloader, sender):
        try:
            result = await downloader.download_audio(url)
        except Exception as e:
            raise UnsupportedMediaType("Audio not available for this Threads post.") from e

        debug("[Threads] audio downloaded")

        audio_path = result.first_media_path()
        await sender.send_audio(audio_path)        


_DISPATCHER = ThreadsDispatcher()
_AUDIO_DISPATCHER = ThreadsAudioDispatcher()

async def handle_threads(update, context, url):
    return await _DISPATCHER.run(update, context, url)

async def handle_threads_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
