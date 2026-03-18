from downloaders.ninegag_downloader import NineGagDownloader
from handlers.dispatchers.base import BaseDispatcher
from models.user_feedback import UnsupportedMediaType
from services.caption_builder import build_9gag_caption
from services.logger import debug


class NineGagDispatcher(BaseDispatcher):
    service_name = "9GAG"

    def create_downloader(self):
        return NineGagDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)
        title = result.title
        content = result.content
        user = result.user
        media_list = result.media

        caption = build_9gag_caption(title, content, user, url)

        await self.send_message(sender, media_list, caption)


class NineGagAudioDispatcher(BaseDispatcher):
    service_name = "9GAG"

    def create_downloader(self):
        return NineGagDownloader()

    async def process(self, update, context, url, downloader, sender):
        try:
            result = await downloader.download_audio(url)
        except Exception as e:
            raise UnsupportedMediaType("Audio not available for this 9GAG post.") from e

        debug("[9GAG] audio downloaded")

        audio_path = result.first_media_path()
        
        await sender.send_audio(audio_path)              


_DISPATCHER = NineGagDispatcher()
_AUDIO_DISPATCHER = NineGagAudioDispatcher()

async def handle_9gag(update, context, url):
    return await _DISPATCHER.run(update, context, url)

async def handle_9gag_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)    
