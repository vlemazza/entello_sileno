from downloaders.bluesky_downloader import BlueSkyVideoDownloader
from services.caption_builder import build_bluesky_captions
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_bluesky(update, context, url):
    downloader = BlueSkyVideoDownloader()
    sender = TelegramMediaSender(update, "Bluesky")

    try:
        result_post = await downloader.download_bluesky_post(url)
        content = result_post["content"]
        user = result_post["user"]

        debug("[Bluesky] post metadata scaricato")

        if result_post["media"]:
            result_media = await downloader.download_bluesky_media(url)
            media_list = result_media["media"]

            debug("[Bluesky] media scaricato")
        else:
            media_list = []
            debug("[Bluesky] no media solo testo")

        caption1, caption2 = build_bluesky_captions(content, user, url)

        if not media_list:
            await sender.send_text(caption1, parse_mode="HTML")
            if caption2:
                await sender.send_text(caption2, parse_mode="HTML")
            return

        if len(media_list) == 1:
            await sender.send_media_list(media_list, caption=caption1, parse_mode="HTML")
            if caption2:
                await sender.send_text(caption2, parse_mode="HTML")
            return

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
        error("[Bluesky] Errore nel download: %s", e)
        await update.message.reply_text(
            "[Bluesky] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )
    finally:
        downloader.cleanup()
        debug("[Bluesky] cleanup completato")
