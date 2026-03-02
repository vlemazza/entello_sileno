from downloaders.media_downloader import MediaDownloader
from handlers.dispatchers.base import BaseDispatcher
from utils.logger import debug, error


class GenericDispatcher(BaseDispatcher):
    service_name = "Generic"

    def create_downloader(self):
        return MediaDownloader()

    async def process(self, update, context, url, downloader, sender):
        try:
            video_path = await downloader.download_video(url)

            debug("[Generic] video downloaded")

            await sender.send_video(video_path)
        except Exception as e:
            error("[Generic] Error download video %s", e)


_DISPATCHER = GenericDispatcher()


async def handle_generic(update, context, url):
    return await _DISPATCHER.run(update, context, url)
