from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes
from utils.logger import debug

async def handle_bot_added_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    member_update = update.my_chat_member

    if chat is None or member_update is None:
        return

    if chat.type not in {"group", "supergroup"}:
        return

    old_status = member_update.old_chat_member.status
    new_status = member_update.new_chat_member.status

    if not(old_status == ChatMemberStatus.LEFT and new_status == ChatMemberStatus.MEMBER):
        return

    debug("[Events] bot aggiunto nel gruppo %s", chat.id)

    await chat.send_message(
        "La scimmia è con te!.\n\n"
        "Manda un link e lo scaricherà.\n\n"

        "*Supporto:*\n"
            "- YouTube  video, audio\n"
            "- Instagram  video, immagini\n"
            "- TikTok  video, immagini\n"
            "- Reddit  video, immagini\n"
            "- Twitter  video, immagini, testo e fanculo Musk\n\n"

        "*Prossimamente:*\n"
            "- Facebook\n"
            "- Threads\n"
            "- Vines\n"
            "- Bluesky\n\n"

        "Chiedete e sarà aggiunto\n\n"

        "*How to asteriscare:*\n"
        "- `*` prima di un link YouTube scarica solo audio\n"
        "  esempio: `*https://www.youtube.com/watch?v=dQw4w9WgXcQ`\n\n"

        "- `**` prima di qualsiasi link ci prova comunque\n"
        "  esempio: `**https://alavi.me/blog/e-ink-tablet-as-monitor-linux/`\n\n"

        "Nessuna scimmia viene maltratta!\n\n"

        "open source [repo github](https://github.com/vlemazza/entello_sileno)",

        parse_mode="Markdown"
)