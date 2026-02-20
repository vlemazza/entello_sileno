from downloaders.reddit_downloader import RedditDownloader
from services.caption_builder import build_reddit_caption
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_reddit(update, context, url):
    downloader = RedditDownloader()
    sender = TelegramMediaSender(update, "Reddit")

    try:
        result = await downloader.download_post(url)
        media_list = result["media"]
        title = result["title"]

        debug("[Reddit] media scaricato")

        caption = build_reddit_caption(title, url)
        await sender.send_media_list(
            media_list,
            caption=caption,
            parse_mode="Markdown",
        )

    except Exception as e:
        error("[Reddit] Errore nel download: %s", e)
        await update.message.reply_text(
            "[Reddit] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )
    finally:
        downloader.cleanup()
        debug("[Reddit] cleanup completato")
