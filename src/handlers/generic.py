from downloaders.video_downloader import VideoDownloader
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_generic(update, context, url):
    downloader = VideoDownloader()
    sender = TelegramMediaSender(update, "Generic")

    try:
        result = await downloader.download_video(url)
        video_path = result["media"][0]["file_path"]

        debug("[Generic] video downloaded")

        await sender.send_video(video_path)

    except Exception as e:
        error("[Generic] Error download video %s", exc)
        return

    finally:
        downloader.cleanup()
        debug("[Generic] video cleanup")
