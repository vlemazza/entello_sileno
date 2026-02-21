from downloaders.instagram_downloader import InstagramDownloader
from services.caption_builder import build_instagram_caption
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_instagram(update, context, url):
    downloader = InstagramDownloader()
    sender = TelegramMediaSender(update, "Instagram")

    try:
        result = await downloader.download_post(url)
        media_list = result["media"]
        title = result["title"]
        description = result["description"][:800]
        author = result["author"]

        debug("[Instagram] media scaricato")

        caption = build_instagram_caption(title, description, author, url)
        await sender.send_media_list(
            media_list,
            caption=caption,
            parse_mode="HTML",
        )

    except Exception as e:
        error("[Instagram] Errore nel download: %s", e)
        await update.message.reply_text(
            "[Instagram] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )
    finally:
        downloader.cleanup()
        debug("[Instagram] cleanup completato")
