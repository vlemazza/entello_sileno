import random
from handlers.dispatchers.generic import handle_generic
from handlers.dispatchers.supported_service import Service
from utils.logger import debug
from utils.urls import extract_domain, extract_url
from services.db.dao_db import is_downloader_disabled
from utils.waiting_message_loader import get_waiting_messages
from handlers.incoming_message import incoming_message

def resolve_handler(url):
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
        target_url = normalizer(clean_url) if normalizer else clean_url
    except Exception as exc:
        debug("[Dispatchers] normalize failed for %s: %s", service_info["name"], exc)
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

    source_service, handler, target_url = resolve_handler(url)
    if handler is None:
        return

    if is_downloader_disabled(update.effective_chat.id, source_service):
        debug("[Dispatchers] %s disabled, chat id: %s", source_service, update.effective_chat.id)
        return

    debug("[Dispatchers] detected %s url", source_service)

    waiting_texts = await get_waiting_messages()
    waiting_message = await update.message.reply_text(
        random.choice(waiting_texts),
        reply_to_message_id=update.message.message_id,
    )

    try:
        await handler(update, context, target_url)
    finally:
        await waiting_message.delete()
