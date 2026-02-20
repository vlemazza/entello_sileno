from downloaders.youtube_downloader import YouTubeDownloader
from services.caption_builder import build_youtube_caption
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_youtube_video(update, context, url):
    downloader = YouTubeDownloader()
    sender = TelegramMediaSender(update, "YouTube")

    try:
        result = downloader.download_video(url)
        video_path = result["media"][0]["file_path"]
        title = result["title"]
        description = result["description"][:800]
        author = result["author"]

        debug("[YouTube] video downloaded")

        caption = build_youtube_caption(title, description, author, url)
        await sender.send_video(video_path, caption=caption, parse_mode="HTML")
    except Exception as e:
        error("[YouTube] Error download video %s", exc)
        return

    finally:
        downloader.cleanup()
        debug("[YouTube] video cleanup")

async def handle_youtube_audio(update, context, url):
    downloader = YouTubeDownloader()
    sender = TelegramMediaSender(update, "YouTube")

    try:
        result = downloader.download_audio(url)
        audio_path = result["media"][0]["file_path"]

        debug("[YouTube] audio downloaded")

        await sender.send_audio(audio_path)

    except Exception as e:
        error("[YouTube] Error download audio %s", exc)
        return

    finally:
        downloader.cleanup()
        debug("[YouTube] audio cleanup")
