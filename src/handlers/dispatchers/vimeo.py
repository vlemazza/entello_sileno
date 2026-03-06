from downloaders.vimeo_downloader import VimeoDownloader
from handlers.dispatchers.base import BaseDispatcher
from models.download_result import DownloadResult
from services.caption_builder import build_vimeo_caption
from services.logger import debug


class VimeoVideoDispatcher(BaseDispatcher):
    service_name = "Vimeo"

    def create_downloader(self):
        return VimeoDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.download_video(url)
        video_path = result.first_media_path()
        title = result.title
        content = result.content
        user = result.user

        debug("[Vimeo] video downloaded")

        caption = build_vimeo_caption(title, content, user, url)
        await self.send_message(
            sender,
            DownloadResult.from_single(video_path, "video").media,
            caption,
        )


class VimeoAudioDispatcher(BaseDispatcher):
    service_name = "Vimeo"

    def create_downloader(self):
        return VimeoDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.download_audio(url)
        audio_path = result.first_media_path()

        debug("[Vimeo] audio downloaded")
        await sender.send_audio(audio_path)


_VIDEO_DISPATCHER = VimeoVideoDispatcher()
_AUDIO_DISPATCHER = VimeoAudioDispatcher()


async def handle_vimeo_video(update, context, url):
    return await _VIDEO_DISPATCHER.run(update, context, url)


async def handle_vimeo_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
