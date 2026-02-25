from downloaders.threads_downloader import ThreadsDownloader
from services.caption_builder import build_threads_captions
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error


async def handle_threads(update, context, url):
    downloader = ThreadsDownloader()
    sender = TelegramMediaSender(update, "Threads")

    try:
        result_post = downloader.download_post(url)

        content = result_post.get("description", "")
        user = result_post.get("author", "")
        media_list = result_post.get("media", [])

        debug("[Threads] post metadata scaricato")

        caption1, caption2 = build_threads_captions(content, user, url)

        if not media_list:
            debug("[Threads] no media solo testo")

            await sender.send_text(caption1, parse_mode="HTML")
            if caption2:
                await sender.send_text(caption2, parse_mode="HTML")
            return

        if len(media_list) == 1:
            debug("[Threads] un solo media")

            await sender.send_media_list(
                media_list,
                caption=caption1,
                parse_mode="HTML"
            )

            if caption2:
                await sender.send_text(caption2, parse_mode="HTML")

            return

        debug("[Threads] media multipli")

        if caption2:
            await sender.send_text(caption1, parse_mode="HTML")
            await sender.send_text(caption2, parse_mode="HTML")
        else:
            await sender.send_text(caption1, parse_mode="HTML")

        await sender.send_media_list(
            media_list,
            caption=None,
            parse_mode="HTML",
        )

    except Exception as e:
        error("[Threads] Errore nel download: %s", e)
        await update.message.reply_text(
            "[Threads] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )
    finally:
        downloader.cleanup()
        debug("[Threads] cleanup completato")