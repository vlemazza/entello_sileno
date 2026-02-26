from downloaders.reddit_downloader import RedditDownloader
from services.caption_builder import build_reddit_caption
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_reddit(update, context, url):
    downloader = RedditDownloader()
    sender = TelegramMediaSender(update, "Reddit")

    try:
        result = downloader.download_post(url)

        media_list = result.get("media", [])
        title = result.get("title", "")
        description = result.get("description", "")
        external_url = result.get("external_url", "")
        author = result.get("author", "")
        subreddit = result.get("subreddit", "")

        caption = build_reddit_caption(
            title,
            description,
            external_url,
            author,
            subreddit,
            url
        )

        if not media_list:
            debug("[Reddit] solo testo")

            await sender.send_text(caption, parse_mode="HTML")
            return

        if len(media_list) == 1:
            media_type = media_list[0].get("type", "")

            if media_type == "video":
                debug("[Reddit] singolo video")
            elif media_type == "image":
                debug("[Reddit] singola immagine")

            await sender.send_media_list(
                media_list,
                caption=caption,
                parse_mode="HTML"
            )
            return

        debug("[Reddit] media multipli")

        await sender.send_text(caption, parse_mode="HTML")
        await sender.send_media_list(
            media_list,
            caption=None,
            parse_mode="HTML"
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
