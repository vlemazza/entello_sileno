from telegram.ext import ApplicationBuilder, MessageHandler, filters
from handlers.dispatchers import url_handler
import os

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, url_handler))

    app.run_polling()
