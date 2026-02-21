from telegram import Update
import os
import time
from utils.logger import debug

MEME = {
    "banana.opus": ["🍌", "banana", "banan"],
    "india.opus": ["🇮🇳", "india", "dosti"],
    "captain.opus": ["captain", "capitano"],
    "stelio.opus": ["stelio", "kontos"],
}

COOLDOWN_GROUPS = {}
COOLDOWN_SECONDS = 300


async def check_meme(update, text):
    text = text.lower()
    actual_time=time.time()
    for audio_file, triggers in MEME.items():
        if any(trigger in text for trigger in triggers):
            last_sent_meme_key=(update.effective_chat.id, audio_file)
            last_sent_meme=COOLDOWN_GROUPS.get(last_sent_meme_key, 0)
            if(actual_time - last_sent_meme >= COOLDOWN_SECONDS):
                if os.path.exists("/audio/" + audio_file):
                    with open("/audio/" + audio_file, "rb") as audio:
                        COOLDOWN_GROUPS[last_sent_meme_key]=actual_time
                        await update.message.reply_audio(
                            audio=audio,
                            reply_to_message_id=update.message.message_id
                        )
                else:
                    await update.message.reply_text(f"{audio_file} not found")
            else:
                return

            return