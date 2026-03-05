from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes
from services.logger import debug

async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    await chat.send_message(
        "La scimmia è con te!\n\n"
        "Scaricherà i media e il testo associato.\n\n"

        "*Siti supportati:*\n"
            "- YouTube\n"
            "- Instagram\n"
            "- TikTok\n"
            "- Reddit\n"
            "- Twitter\n"
            "- Bluesky\n"
            "- Facebook\n"
            "- Threads\n\n"

        "*How to asteriscare:*\n"
        "- `*` prima di un link scarica solo audio\n"
        "  esempio: `*https://www.youtube.com/watch?v=dQw4w9WgXcQ`\n\n"

        "- `**` prima di qualsiasi link ci prova anche se non supportato\n"
        "  esempio: `**https://alavi.me/blog/e-ink-tablet-as-monitor-linux/`\n\n"

        "*Comandi:*\n"
        "- /settings modificare impostazioni per chat.\n"
        "- /help invia questo help.\n\n"

        "Nessuna scimmia viene maltrattata!\n\n"

        "### open source [repo github](https://github.com/vlemazza/entello_sileno) ###",

        parse_mode="Markdown",
        disable_web_page_preview=True,
)