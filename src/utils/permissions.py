import os
from telegram import Update

whitelist_user = [x.strip() for x in os.getenv("WHITELIST_USER", "").split(",") if x]
whitelist_group = [x.strip() for x in os.getenv("WHITELIST_GROUP", "").split(",") if x]

async def chat_not_in_list(chat_id, user_id):

    if str(chat_id) in whitelist_group or str(user_id) in whitelist_user:
        return False

    return True    

async def inform_user(update):

    if update.effective_chat.type == "private":
        await update.message.reply_text(
            f"La scimmia dice NO\n "
            f"[Username]:  {update.effective_user.username}\n "
            f"[Chat ID]: {update.effective_chat.id}",
            reply_to_message_id=update.message.message_id,
        )