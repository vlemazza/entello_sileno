#from downloaders.video_downloader import VideoDownloader
from downloaders.facebook_downloader import FacebookDownloader
from services.caption_builder import build_facebook_caption
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_facebook(update, context, url):
    downloader = FacebookDownloader()
    sender = TelegramMediaSender(update, "Facebook")

    try:
        result = await downloader.download_post(url)
        media_list = result["media"]
        title = result["title"]
        description = result["description"][:800]
        author = result["author"]

        debug("[Facebook] media scaricato")

        caption = build_facebook_caption(title, description, author, url)
        await sender.send_media_list(
            media_list,
            caption=caption,
            parse_mode="HTML",
        )

    except Exception as e:
        error("[Facebook] Errore nel download: %s", e)
        await update.message.reply_text(
            "[Facebook] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )
    finally:
        downloader.cleanup()
        debug("[Facebook] cleanup completato")

