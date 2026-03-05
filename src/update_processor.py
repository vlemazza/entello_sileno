import asyncio
from telegram.ext import BaseUpdateProcessor


class EntelloUpdateProcessor(BaseUpdateProcessor):
    async def do_process_update(self, update, coroutine):
        if getattr(update, "callback_query", None):
            await asyncio.sleep(1)

        await coroutine

    async def initialize(self):
        return None

    async def shutdown(self):
        return None
