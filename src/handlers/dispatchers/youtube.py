from downloaders.youtube_downloader import YouTubeDownloader
from handlers.dispatchers.base import BaseDispatcher
from models.download_result import DownloadResult
from services.caption_builder import build_youtube_caption
from utils.logger import debug


class YouTubeVideoDispatcher(BaseDispatcher):
    service_name = "YouTube"

    def create_downloader(self):
        return YouTubeDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.download_video(url)
        video_path = result.first_media_path()
        title = result.title
        description = result.description[:800]
        author = result.author

        debug("[YouTube] video downloaded")

        caption = build_youtube_caption(title, description, author, url)
        await self.send_message(
            sender,
            DownloadResult.from_single(video_path, "video").media,
            caption,
        )


class YouTubeAudioDispatcher(BaseDispatcher):
    service_name = "YouTube"

    def create_downloader(self):
        return YouTubeDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = downloader.download_audio(url)
        audio_path = result.first_media_path()

        debug("[YouTube] audio downloaded")
        await sender.send_audio(audio_path)


_VIDEO_DISPATCHER = YouTubeVideoDispatcher()
_AUDIO_DISPATCHER = YouTubeAudioDispatcher()


async def handle_youtube_video(update, context, url):
    return await _VIDEO_DISPATCHER.run(update, context, url)


async def handle_youtube_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
