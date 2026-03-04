from abc import ABC, abstractmethod
from services.caption_splitter import split_html_caption
from services.media_sender import TelegramMediaSender
from services.logger import debug, error, warning
from models.user_feedback import UserFacingError


class BaseDispatcher(ABC):
    service_name = ""
    default_parse_mode = "HTML"
    caption_limit = 1024
    text_limit = 4096
    album_chunk = 10

    def create_sender(self, update):
        return TelegramMediaSender(update, self.service_name)

    @abstractmethod
    def create_downloader(self):
        pass

    @abstractmethod
    async def process(self, update, context, url, downloader, sender):
        pass

    async def run(self, update, context, url):
        downloader = self.create_downloader()
        sender = self.create_sender(update)

        try:
            return await self.process(update, context, url, downloader, sender)
        except UserFacingError as e:
            await sender.send_text(e.user_message)
        except Exception as e:
            error("[%s] Error download: %s", self.service_name, e)
        finally:
            downloader.cleanup()
            debug("[%s] cleanup", self.service_name)

    def _as_media_dicts(self, media_items):
        return [{"file_path": m.file_path, "type": m.type} for m in media_items]

    async def _send_texts(self, sender, captions, parse_mode=None):
        mode = parse_mode or self.default_parse_mode
        for text in [c for c in captions if c]:
            await sender.send_text(text, parse_mode=mode)

    async def _send_media(self, sender, media_items, caption=None, parse_mode=None):
        mode = parse_mode or self.default_parse_mode
        await sender.send_media_list(
            self._as_media_dicts(media_items),
            caption=caption,
            parse_mode=mode,
        )

    async def send_message(self, sender, media_items, caption, parse_mode=None):
        mode = parse_mode or self.default_parse_mode
        if caption:
            text_chunks = split_html_caption(caption, self.text_limit)
        else:
            text_chunks = []

        if not media_items:
            await self._send_texts(sender, text_chunks, parse_mode=mode)
            return

        if len(media_items) > self.album_chunk:
            await self._send_media(sender, media_items, caption=None, parse_mode=mode)
            await self._send_texts(sender, text_chunks, parse_mode=mode)
            return

        first_caption = text_chunks[0] if text_chunks else None
        if first_caption and len(first_caption) <= self.caption_limit:
            await self._send_media(sender, media_items, caption=first_caption, parse_mode=mode)
            await self._send_texts(sender, text_chunks[1:], parse_mode=mode)
            return

        if first_caption:
            caption_parts = split_html_caption(first_caption, self.caption_limit)
            if caption_parts:
                await self._send_media(sender, media_items, caption=caption_parts[0], parse_mode=mode)
                await self._send_texts(sender, caption_parts[1:] + text_chunks[1:], parse_mode=mode)
                return

        await self._send_media(sender, media_items, caption=None, parse_mode=mode)
        await self._send_texts(sender, text_chunks, parse_mode=mode)
