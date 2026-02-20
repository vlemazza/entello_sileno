from telegram import Update
import os

MEME = {
    "banana.opus": ["🍌", "banana", "banan"],
    "india.opus": ["🇮🇳", "india", "dosti"],
    "captain.opus": ["captain", "capitano"],
    "stelio.opus": ["stelio", "kontos"],
}

async def check_meme(update, text):
    text = text.lower()

    for audio_file, triggers in MEME.items():
        if any(trigger in text for trigger in triggers):
            if os.path.exists(audio_file):
                with open(audio_file, "rb") as audio:
                    await update.message.reply_audio(
                        audio=audio,
                        reply_to_message_id=update.message.message_id
                    )
            else:
                await update.message.reply_text(f"{audio_file} not found")

            return