from downloaders.youtube_downloader import YouTubeDownloader
from services.caption_builder import build_youtube_caption
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error
from yt_dlp.utils import DownloadError

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
    except DownloadError, Exception as e:
        error("[YouTube] Error download video %s", e)
        await update.message.reply_text(
            "[YouTube] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )

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

    except DownloadError, Exception as e:
        error("[YouTube] Error download video %s", e)
        await update.message.reply_text(
            "[YouTube] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )

    finally:
        downloader.cleanup()
        debug("[YouTube] audio cleanup")
