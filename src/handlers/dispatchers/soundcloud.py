from downloaders.soundcloud_downloader import SoundCloudDownloader
from handlers.dispatchers.base import BaseDispatcher
from services.caption_builder import build_soundcloud_caption
from services.logger import debug


class SoundCloudAudioDispatcher(BaseDispatcher):
    service_name = "SoundCloud"

    def create_downloader(self):
        return SoundCloudDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_audio(url)
        caption = build_soundcloud_caption(result.title, result.content, result.user, url)

        debug("[SoundCloud] audio downloaded")
        audio_path = result.first_media_path()
        await sender.send_audio(audio_path, caption=caption, parse_mode=self.default_parse_mode)


_AUDIO_DISPATCHER = SoundCloudAudioDispatcher()


async def handle_soundcloud_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
