import random
from utils.extract_url import extract_url
from utils.extract_url import check_url_twitter
from utils.text_meme import check_meme
from utils.logger import debug
from handlers.youtube import handle_youtube_video, handle_youtube_audio
from handlers.instagram import handle_instagram
from handlers.tiktok import handle_tiktok
from handlers.reddit import handle_reddit
from handlers.twitter import handle_twitter
from handlers.generic import handle_generic
from utils.waiting_message_loader import get_waiting_messages
from utils.permissions import chat_not_in_list, inform_user

def resolve_handler(url):
    if "**" in url:
        return "generic", handle_generic, url.lstrip("*")

    if "youtube.com" in url or "youtu.be" in url:
        if "*" in url:
            return "youtube audio", handle_youtube_audio, url.lstrip("*")
        return "youtube video", handle_youtube_video, url

    if "instagram.com" in url:
        return "instagram", handle_instagram, url

    if "tiktok.com" in url:
        return "tiktok", handle_tiktok, url

    if "reddit.com" in url:
        return "reddit", handle_reddit, url

    if "x.com" in url or "nitter.poast.org" in url:
        if not check_url_twitter(url):
            return None, None, None
        else:
            normalized_url = url.replace("nitter.poast.org", "x.com")
            return "twitter", handle_twitter, normalized_url

    return None, None, None


async def url_handler(update, context):
    message = update.message
    if message is None or message.text is None:
        return

    if await chat_not_in_list(update.effective_chat.id, update.effective_user.id):
        await inform_user(update)
        return

    text = message.text

    await check_meme(update, text)

    url = extract_url(text)
    if not url:
        return

    source, handler, target_url = resolve_handler(url)
    if handler is None:
        return

    debug("[Dispatchers] detected %s url", source)

    waiting_texts = await get_waiting_messages()
    waiting_message = await update.message.reply_text(
        random.choice(waiting_texts),
        reply_to_message_id=update.message.message_id,
    )

    try:
        await handler(update, context, target_url)
    finally:
        await waiting_message.delete()
