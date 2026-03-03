from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.db.dao_db import (
    SUPPORTED_DOWNLOADERS,
    get_chat_settings,
    toggle_downloader,
    toggle_memes,
)

DOWNLOADER_LABELS = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "reddit": "Reddit",
    "twitter": "Twitter",
    "bluesky": "Bluesky",
    "facebook": "Facebook",
    "threads": "Threads",
    "generic": "Generic (**)",
}


def _build_settings_keyboard(chat_id: int):
    settings = get_chat_settings(chat_id)

    meme_label = "Meme: ON" if settings.memes_enabled else "Meme: OFF"
    rows = [
        [InlineKeyboardButton(meme_label, callback_data="settings:toggle:meme")],
    ]

    for downloader in SUPPORTED_DOWNLOADERS:
        enabled = downloader not in settings.disabled_downloaders
        status = "ON" if enabled else "OFF"
        label = f"{DOWNLOADER_LABELS[downloader]}: {status}"
        rows.append(
            [
                InlineKeyboardButton(
                    label,
                    callback_data=f"settings:toggle:downloader:{downloader}",
                )
            ]
        )

    return InlineKeyboardMarkup(rows)


def _build_settings_text(chat_id: int):
    settings = get_chat_settings(chat_id)
    disabled = sorted(settings.disabled_downloaders)
    disabled_labels = (
        ", ".join(DOWNLOADER_LABELS[item] for item in disabled)
        if disabled
        else "Nessuno"
    )

    meme_state = "abilitati" if settings.memes_enabled else "disabilitati"
    return (
        "*Impostazioni chat*\n\n"
        f"- Meme: {meme_state}\n"
        f"- Downloader disabilitati: {disabled_labels}\n\n"
    )


async def handle_settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None or update.message is None:
        return

    chat_id = update.effective_chat.id
    await update.message.reply_text(
        _build_settings_text(chat_id),
        parse_mode="Markdown",
        reply_markup=_build_settings_keyboard(chat_id),
    )


async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None or query.data is None:
        return

    if not query.data.startswith("settings:toggle:"):
        return

    if query.message is None or query.message.chat is None:
        await query.answer("Errore: chat non trovata", show_alert=True)
        return

    chat_id = query.message.chat.id
    parts = query.data.split(":")

    try:
        if len(parts) == 3 and parts[2] == "meme":
            enabled = toggle_memes(chat_id)
            await query.answer("Meme attivati" if enabled else "Meme disattivati")
        elif len(parts) == 4 and parts[2] == "downloader":
            downloader = parts[3]
            disabled = toggle_downloader(chat_id, downloader)
            status_text = "disabilitato" if disabled else "riattivato"
            await query.answer(f"{DOWNLOADER_LABELS[downloader]} {status_text}")
        else:
            await query.answer("Azione non valida", show_alert=True)
            return
    except ValueError:
        await query.answer("Downloader non supportato", show_alert=True)
        return

    await query.edit_message_text(
        _build_settings_text(chat_id),
        parse_mode="Markdown",
        reply_markup=_build_settings_keyboard(chat_id),
    )
