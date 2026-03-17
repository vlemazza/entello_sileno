from downloaders.peertube_downloader import PeerTubeDownloader
from handlers.dispatchers.base import BaseDispatcher
from models.download_result import DownloadResult
from services.caption_builder import build_peertube_caption
from services.logger import debug


class PeerTubeVideoDispatcher(BaseDispatcher):
    service_name = "PeerTube"

    def create_downloader(self):
        return PeerTubeDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.download_video(url)
        video_path = result.first_media_path()
        title = result.title
        content = result.content
        user = result.user

        debug("[PeerTube] video downloaded")

        caption = build_peertube_caption(title, content, user, url)
        await self.send_message(
            sender,
            DownloadResult.from_single(video_path, "video").media,
            caption,
        )


class PeerTubeAudioDispatcher(BaseDispatcher):
    service_name = "PeerTube"

    def create_downloader(self):
        return PeerTubeDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.download_audio(url)
        audio_path = result.first_media_path()

        debug("[PeerTube] audio downloaded")
        await sender.send_audio(audio_path)


_VIDEO_DISPATCHER = PeerTubeVideoDispatcher()
_AUDIO_DISPATCHER = PeerTubeAudioDispatcher()


async def handle_peertube_video(update, context, url):
    return await _VIDEO_DISPATCHER.run(update, context, url)


async def handle_peertube_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
