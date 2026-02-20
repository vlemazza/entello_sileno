import requests
from downloaders.tiktok_downloader import TikTokDownloader
from services.caption_builder import build_tiktok_photo_caption, build_tiktok_video_caption
from services.media_sender import TelegramMediaSender
from utils.logger import debug, error

async def handle_tiktok(update, context, url):
    final_url = requests.head(url, allow_redirects=True).url
    downloader = TikTokDownloader()
    sender = TelegramMediaSender(update, "TikTok")

    try:
        if "/photo/" in final_url:
            result = downloader.download_photos(url)
            media_list = result["media"]
            title = result["title"]
            description = result["description"]
            author = result["author"]

            debug("[TikTok] image downloaded")

            caption = build_tiktok_photo_caption(title, description, author, final_url)
            photo_list = [
                media
                for media in media_list
                if media["type"] == "image"
            ]
            audio_paths = [
                media["file_path"]
                for media in media_list
                if media["type"] == "audio"
            ]

            await sender.send_media_list(
                photo_list,
                caption=caption,
                parse_mode="HTML",
            )
            for audio_path in audio_paths:
                await sender.send_audio(audio_path)

        else:
            result = downloader.download_video(final_url)
            video_path = result["media"][0]["file_path"]
            title = result["title"]
            description = result["description"]
            author = result["author"]

            debug("[TikTok] video downloaded")
            caption = build_tiktok_video_caption(title, description, author, final_url)
            await sender.send_video(video_path, caption=caption, parse_mode="HTML")

    except Exception as e:
        error("[TikTok] Error download: %s", exc)
        await update.message.reply_text(
            "[TikTok] Errore durante il download del contenuto.",
            reply_to_message_id=update.message.message_id
        )

    finally:
        downloader.cleanup()
        debug("[TikTok] cleanup completato")
