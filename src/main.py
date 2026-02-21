from telegram.ext import ApplicationBuilder, ChatMemberHandler, MessageHandler, filters
from handlers.dispatchers.dispatchers import url_handler
from handlers.events import handle_bot_added_group
import os

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatMemberHandler(handle_bot_added_group, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, url_handler))

    app.run_polling()
