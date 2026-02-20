from telegram import InputMediaPhoto, InputMediaVideo
from telegram.error import NetworkError, TelegramError, TimedOut
from utils.logger import error

STICKER_PATH = "sticker.webp"


class TelegramMediaSender:
    def __init__(self, update, source_name):
        self.update = update
        self.message = update.message
        self.source_name = source_name

    async def send_video(self, video_path, caption=None, parse_mode=None):
        try:
            with open(video_path, "rb") as video_file:
                await self.message.chat.send_video(
                    video=video_file,
                    disable_notification=True,
                    caption=caption,
                    parse_mode=parse_mode,
                    reply_to_message_id=self.message.message_id,
                )
        except TimedOut as e:
            error("[%s] Timeout while sending video. %s", self.source_name, e)
        except Exception as e:
            await self._reply_error(f"[{self.source_name}] Error sending video: {e}")

    async def send_audio(self, audio_path, caption=None, parse_mode=None):
        try:
            with open(audio_path, "rb") as audio_file:
                await self.message.chat.send_audio(
                    audio=audio_file,
                    caption=caption,
                    parse_mode=parse_mode,
                    disable_notification=True,
                    reply_to_message_id=self.message.message_id,
                )
        except TimedOut as e:
            error("[%s] Timeout while sending audio. %s", self.source_name, e)
        except Exception as e:
            await self._reply_error(f"[{self.source_name}] Error sending audio: {e}")

    async def send_text(self, text, parse_mode=None):
        await self.message.reply_text(
            text=text,
            parse_mode=parse_mode,
            reply_to_message_id=self.message.message_id,
        )

    async def send_media_list(
        self,
        media_list,
        caption=None,
        parse_mode=None,
    ):
        if not media_list:
            return

        try:
            if len(media_list) == 1:
                await self._send_single_media(
                    media=media_list[0],
                    caption=caption,
                    parse_mode=parse_mode,
                )
                return

            total = len(media_list)
            for chunk_start in range(0, total, 10):
                chunk = media_list[chunk_start : chunk_start + 10]
                album = []

                for i, media in enumerate(chunk):
                    with open(media["file_path"], "rb") as media_file:
                        data = media_file.read()

                    item_caption = self._resolve_caption(
                        caption=caption,
                        chunk_start=chunk_start,
                        index_in_chunk=i,
                    )

                    if media["type"] == "image":
                        album.append(
                            InputMediaPhoto(
                                media=data,
                                caption=item_caption,
                                parse_mode=parse_mode if item_caption else None,
                            )
                        )
                    elif media["type"] == "video":
                        album.append(
                            InputMediaVideo(
                                media=data,
                                caption=item_caption,
                                parse_mode=parse_mode if item_caption else None,
                            )
                        )

                await self.message.chat.send_media_group(
                    media=album,
                    disable_notification=True,
                    reply_to_message_id=self.message.message_id,
                )
        except Exception as e:
            error("[%s] Error sending media list: %s", self.source_name, e)
            await self._reply_error(f"[{self.source_name}] Errore durante l'invio del contenuto.")

    async def _send_single_media(self, media, caption=None, parse_mode=None):
        with open(media["file_path"], "rb") as media_file:
            if media["type"] == "image":
                await self.message.chat.send_photo(
                    photo=media_file,
                    caption=caption,
                    parse_mode=parse_mode,
                    disable_notification=True,
                    reply_to_message_id=self.message.message_id,
                )
            elif media["type"] == "video":
                await self.message.chat.send_video(
                    video=media_file,
                    caption=caption,
                    parse_mode=parse_mode,
                    disable_notification=True,
                    reply_to_message_id=self.message.message_id,
                )

    def _resolve_caption(
        self,
        caption,
        chunk_start,
        index_in_chunk,
    ):
        if not caption:
            return None

        return caption if chunk_start == 0 and index_in_chunk == 0 else None

    async def _reply_error(self, text):
        try:
            with open(STICKER_PATH, "rb") as sticker_file:
                await self.message.reply_sticker(
                    sticker=sticker_file,
                    reply_to_message_id=self.message.message_id,
                )
        except Exception as e:
            error("[%s] Error sending sticker: %s", self.source_name, e)
            await self.message.reply_text(
                text,
                reply_to_message_id=self.message.message_id,
            )
