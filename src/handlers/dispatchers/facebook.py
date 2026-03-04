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
        content = result.content
        user = result.user

        debug("[Facebook] media downloaded")

        caption = build_facebook_caption(title, content, user, url)
        
        await self.send_message(sender, media_list, caption)

class FacebookAudioDispatcher(BaseDispatcher):
    service_name = "Facebook"

    def create_downloader(self):
        return FacebookDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.download_audio(url, impersonate=True)
        debug("[Facebook] audio downloaded")

        audio_path = result.first_media_path()
        
        await sender.send_audio(audio_path)        


_DISPATCHER = FacebookDispatcher()
_AUDIO_DISPATCHER = FacebookAudioDispatcher()



async def handle_facebook(update, context, url):
    return await _DISPATCHER.run(update, context, url)

async def handle_facebook_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)    
