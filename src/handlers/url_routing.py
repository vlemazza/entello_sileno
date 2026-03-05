import random
from handlers.dispatchers.generic import handle_generic
from handlers.dispatchers.supported_service import Service
from services.logger import debug
from services.media_sender import TelegramMediaSender
from utils.urls import extract_domain, extract_url
from services.db.dao_db import is_downloader_disabled
from utils.waiting_message_loader import get_waiting_messages
from handlers.incoming_message import incoming_message

async def resolve_handler(url):
    if "**" in url:
        return "generic", handle_generic, url.lstrip("*")

    audio_requested = url.startswith("*")
    clean_url = url.lstrip("*")
    service = _match_service(clean_url)
    if service is None:
        return None, None, None

    service_info = service.value
    normalizer = service_info.get("normalize")

    try:
        target_url = await normalizer(clean_url) if normalizer else clean_url
    except Exception as e:
        debug("[Dispatchers] normalize failed for %s: %s", service_info["name"], e)
        return None, None, None

    handler = service_info.get("audio_handler") if audio_requested else service_info.get("handler")
    if handler is None:
        return None, None, None

    return service_info["name"], handler, target_url


def _match_service(clean_url):
    domain = extract_domain(clean_url)
    if domain in Service.YOUTUBE.value["domains"]:
        return Service.YOUTUBE
    elif domain in Service.INSTAGRAM.value["domains"]:
        return Service.INSTAGRAM
    elif domain in Service.FACEBOOK.value["domains"]:
        return Service.FACEBOOK
    elif domain in Service.TIKTOK.value["domains"]:
        return Service.TIKTOK
    elif domain in Service.REDDIT.value["domains"]:
        return Service.REDDIT
    elif domain in Service.TWITTER.value["domains"]:
        return Service.TWITTER
    elif domain in Service.BLUESKY.value["domains"]:
        return Service.BLUESKY
    elif domain in Service.THREADS.value["domains"]:
        return Service.THREADS
    else:
        return None


async def url_handler(update, context):
    text = await incoming_message(update)
    if text is None:
        return

    url = extract_url(text)
    if not url:
        return

    source_service, handler, target_url = await resolve_handler(url)
    if handler is None:
        return

    if await is_downloader_disabled(update.effective_chat.id, source_service):
        debug("[Dispatchers] %s disabled, chat id: %s", source_service, update.effective_chat.id)
        return

    debug("[Dispatchers] detected %s url", source_service)

    waiting_texts = await get_waiting_messages()
    sender = TelegramMediaSender(update, source_service)
    try:
        waiting_message = await sender.send_text(random.choice(waiting_texts))
    except Exception as e:
        debug("[Dispatchers] waiting message failed: %s", e)
        waiting_message = None

    try:
        await handler(update, context, target_url)
    finally:
        if waiting_message:
            await waiting_message.delete()
