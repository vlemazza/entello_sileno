from services.db.dao_db import get_chat_settings
from utils.permissions import chat_not_in_list, inform_user, is_group_whitelisted
from utils.text_meme import check_meme


async def incoming_message(update):
    message = update.message
    if message is None or message.text is None:
        return None

    chat = update.effective_chat
    if chat.type in ("group", "supergroup"):
        if not is_group_whitelisted(chat.id):
            return None
    elif await chat_not_in_list(chat.id, update.effective_user.id):
        await inform_user(update)
        return None

    settings = get_chat_settings(update.effective_chat.id)
    text = message.text

    if settings.memes_enabled:
        await check_meme(update, text)

    return text
