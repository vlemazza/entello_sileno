import requests
from downloaders.tiktok_downloader import TikTokDownloader
from handlers.dispatchers.base import BaseDispatcher
from models.download_result import DownloadResult
from services.caption_builder import build_tiktok_photo_caption, build_tiktok_video_caption
from utils.logger import debug


class TikTokVideoDispatcher(BaseDispatcher):
    service_name = "TikTok"

    def create_downloader(self):
        return TikTokDownloader()

    async def process(self, update, context, url, downloader, sender):
        final_url = requests.head(url, allow_redirects=True).url

        if "/photo/" in final_url:
            result = downloader.download_photos(url)
            media_list = result.media
            title = result.title
            description = result.description
            author = result.author

            debug("[TikTok] image downloaded")

            photo_list = [
                media
                for media in media_list
                if media.type == "image"
            ]
            audio_paths = [
                media.file_path
                for media in media_list
                if media.type == "audio"
            ]

            caption = build_tiktok_photo_caption(title, description, author, final_url)
            await self.send_message(sender, photo_list, caption)
            for audio_path in audio_paths:
                await sender.send_audio(audio_path)
            return

        result = await downloader.download_video(final_url)
        video_path = result.first_media_path()
        title = result.title
        description = result.description
        author = result.author

        debug("[TikTok] video downloaded")
        caption = build_tiktok_video_caption(title, description, author, final_url)
        await self.send_message(
            sender,
            DownloadResult.from_single(video_path, "video").media,
            caption,
        )


class TikTokAudioDispatcher(BaseDispatcher):
    service_name = "TikTok"

    def create_downloader(self):
        return TikTokDownloader()

    async def process(self, update, context, url, downloader, sender):
        final_url = requests.head(url, allow_redirects=True).url

        if "/photo/" in final_url:
            return await _VIDEO_DISPATCHER.run(update, context, url)

        result = downloader.download_audio(final_url)
        audio_path = result.first_media_path()

        debug("[TikTok] audio downloaded")
        await sender.send_audio(audio_path)


_VIDEO_DISPATCHER = TikTokVideoDispatcher()
_AUDIO_DISPATCHER = TikTokAudioDispatcher()


async def handle_tiktok(update, context, url):
    return await _VIDEO_DISPATCHER.run(update, context, url)


async def handle_tiktok_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
