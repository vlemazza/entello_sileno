from downloaders.twitter_downloader import TwitterDownloader
from services.caption_builder import build_twitter_captions
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_twitter(update, context, url):
    downloader = TwitterDownloader()
    sender = TelegramMediaSender(update, "Twitter")

    try:
        result_post = await downloader.download_tweet_post(url)
        content = result_post["content"]
        user = result_post["user"]

        debug("[Twitter] post metadata scaricato")

        if result_post["media"]:
            result_media = await downloader.download_tweet_media(url)
            media_list = result_media["media"]

            debug("[Twitter] media scaricato")
        else:
            media_list = []
            debug("[Twitter] no media solo testo")

        caption1, caption2 = build_twitter_captions(content, user, url)

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
        error("[Twitter] Errore nel download: %s", exc)
        await update.message.reply_text(
            "[Twitter] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )
    finally:
        downloader.cleanup()
        debug("[Twitter] cleanup completato")
