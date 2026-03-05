import os
import asyncio
import aiosqlite
from services.db.entity import ChatSettings

class Repository:
    def __init__(self):
        env_db_path = os.getenv("DB_PATH", "").strip()
        self.db_path = env_db_path or "/bot/db/entello.db"
        self._initialized = False
        self._init_lock = asyncio.Lock()

    async def _initialize(self):
        directory = os.path.dirname(self.db_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as conn:
            await self._ensure_schema(conn)
            await conn.commit()

    async def _initialize_once(self):
        if self._initialized:
            return
        async with self._init_lock:
            if self._initialized:
                return
            await self._initialize()
            self._initialized = True

    async def _ensure_schema(self, conn: aiosqlite.Connection):
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_settings (
                chat_id INTEGER PRIMARY KEY,
                memes_enabled INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS disabled_downloaders (
                chat_id INTEGER NOT NULL,
                downloader TEXT NOT NULL,
                PRIMARY KEY(chat_id, downloader),
                FOREIGN KEY(chat_id) REFERENCES chat_settings(chat_id) ON DELETE CASCADE
            )
            """
        )

    async def _ensure_chat_row(self, conn: aiosqlite.Connection, chat_id: int):
        await self._ensure_schema(conn)
        await conn.execute(
            """
            INSERT OR IGNORE INTO chat_settings(chat_id, memes_enabled)
            VALUES (?, 1)
            """,
            (chat_id,),
        )

    async def get_chat_settings(self, chat_id: int):
        await self._initialize_once()
        async with aiosqlite.connect(self.db_path) as conn:
            await self._ensure_chat_row(conn, chat_id)
            row = await conn.execute(
                "SELECT memes_enabled FROM chat_settings WHERE chat_id = ?",
                (chat_id,),
            )
            row = await row.fetchone()
            downloader_rows = await conn.execute(
                "SELECT downloader FROM disabled_downloaders WHERE chat_id = ?",
                (chat_id,),
            )
            downloader_rows = await downloader_rows.fetchall()

            await conn.commit()

        memes_enabled = bool(row[0]) if row else True
        disabled_downloaders = {entry[0] for entry in downloader_rows}
        return ChatSettings(
            chat_id=chat_id,
            memes_enabled=memes_enabled,
            disabled_downloaders=disabled_downloaders,
        )

    async def toggle_memes(self, chat_id: int):
        await self._initialize_once()
        async with aiosqlite.connect(self.db_path) as conn:
            await self._ensure_chat_row(conn, chat_id)
            row = await conn.execute(
                "SELECT memes_enabled FROM chat_settings WHERE chat_id = ?",
                (chat_id,),
            )
            row = await row.fetchone()
            current_value = bool(row[0]) if row else True
            new_value = 0 if current_value else 1

            await conn.execute(
                "UPDATE chat_settings SET memes_enabled = ? WHERE chat_id = ?",
                (new_value, chat_id),
            )
            await conn.commit()

        return bool(new_value)

    async def toggle_downloader(self, chat_id: int, downloader: str):
        await self._initialize_once()
        async with aiosqlite.connect(self.db_path) as conn:
            await self._ensure_chat_row(conn, chat_id)
            row = await conn.execute(
                """
                SELECT 1
                FROM disabled_downloaders
                WHERE chat_id = ? AND downloader = ?
                """,
                (chat_id, downloader),
            )
            row = await row.fetchone()

            if row:
                await conn.execute(
                    """
                    DELETE FROM disabled_downloaders
                    WHERE chat_id = ? AND downloader = ?
                    """,
                    (chat_id, downloader),
                )
                await conn.commit()
                return False

            await conn.execute(
                """
                INSERT INTO disabled_downloaders(chat_id, downloader)
                VALUES (?, ?)
                """,
                (chat_id, downloader),
            )
            await conn.commit()
            return True
