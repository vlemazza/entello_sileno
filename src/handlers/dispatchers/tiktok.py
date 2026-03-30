from downloaders.tiktok_downloader import TikTokDownloader
from handlers.dispatchers.base import BaseDispatcher
from models.download_result import DownloadResult
from services.caption_builder import build_tiktok_photo_caption, build_tiktok_video_caption
from services.logger import debug


class TikTokVideoDispatcher(BaseDispatcher):
    service_name = "TikTok"

    def create_downloader(self):
        return TikTokDownloader()

    async def process(self, update, context, url, downloader, sender):
        result = await downloader.fetch_post(url)
        media_result = await downloader.fetch_media(url)
        media_list = media_result.media
        title = result.title
        content = result.content
        user = result.user

        debug("[TikTok] post downloaded")

        if media_list and media_list[0].type == "image":
            debug("[TikTok] image downloaded")
            photo_list = [m for m in media_list if m.type == "image"]

            caption = build_tiktok_photo_caption(title, content, user, url)
            await self.send_message(sender, photo_list, caption)

            audio_paths = [m.file_path for m in media_list if m.type == "audio"]
            for audio_path in audio_paths:
                await sender.send_audio(audio_path)
            return

        debug("[TikTok] video downloaded")
        caption = build_tiktok_video_caption(title, content, user, url)
        await self.send_message(
            sender,
            media_list,
            caption,
        )


class TikTokAudioDispatcher(BaseDispatcher):
    service_name = "TikTok"

    def create_downloader(self):
        return TikTokDownloader()

    async def process(self, update, context, url, downloader, sender):
        info = await downloader.get_info_from_ytdlp(url)
        final_url = info.get("webpage_url") or info.get("original_url") or url

        if "/photo/" in final_url:
            return await _VIDEO_DISPATCHER.run(update, context, url)

        result = await downloader.download_audio(final_url)
        audio_path = result.first_media_path()

        debug("[TikTok] audio downloaded")
        await sender.send_audio(audio_path)


_VIDEO_DISPATCHER = TikTokVideoDispatcher()
_AUDIO_DISPATCHER = TikTokAudioDispatcher()


async def handle_tiktok(update, context, url):
    return await _VIDEO_DISPATCHER.run(update, context, url)


async def handle_tiktok_audio(update, context, url):
    return await _AUDIO_DISPATCHER.run(update, context, url)
