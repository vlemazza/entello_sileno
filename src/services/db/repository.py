import os
import sqlite3
from services.db.entity import ChatSettings

class Repository:
    def __init__(self):
        env_db_path = os.getenv("DB_PATH", "").strip()
        self.db_path = env_db_path or "/bot/db/entello.db"
        self._initialize()

    def _initialize(self):
        directory = os.path.dirname(self.db_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            self._ensure_schema(conn)
            conn.commit()

    def _ensure_schema(self, conn: sqlite3.Connection):
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_settings (
                chat_id INTEGER PRIMARY KEY,
                memes_enabled INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS disabled_downloaders (
                chat_id INTEGER NOT NULL,
                downloader TEXT NOT NULL,
                PRIMARY KEY(chat_id, downloader),
                FOREIGN KEY(chat_id) REFERENCES chat_settings(chat_id) ON DELETE CASCADE
            )
            """
        )

    def _ensure_chat_row(self, conn: sqlite3.Connection, chat_id: int):
        self._ensure_schema(conn)
        conn.execute(
            """
            INSERT OR IGNORE INTO chat_settings(chat_id, memes_enabled)
            VALUES (?, 1)
            """,
            (chat_id,),
        )

    def get_chat_settings(self, chat_id: int):
        with sqlite3.connect(self.db_path) as conn:
            self._ensure_chat_row(conn, chat_id)
            row = conn.execute(
                "SELECT memes_enabled FROM chat_settings WHERE chat_id = ?",
                (chat_id,),
            ).fetchone()
            downloader_rows = conn.execute(
                "SELECT downloader FROM disabled_downloaders WHERE chat_id = ?",
                (chat_id,),
            ).fetchall()

            conn.commit()

        memes_enabled = bool(row[0]) if row else True
        disabled_downloaders = {entry[0] for entry in downloader_rows}
        return ChatSettings(
            chat_id=chat_id,
            memes_enabled=memes_enabled,
            disabled_downloaders=disabled_downloaders,
        )

    def toggle_memes(self, chat_id: int):
        with sqlite3.connect(self.db_path) as conn:
            self._ensure_chat_row(conn, chat_id)
            row = conn.execute(
                "SELECT memes_enabled FROM chat_settings WHERE chat_id = ?",
                (chat_id,),
            ).fetchone()
            current_value = bool(row[0]) if row else True
            new_value = 0 if current_value else 1

            conn.execute(
                "UPDATE chat_settings SET memes_enabled = ? WHERE chat_id = ?",
                (new_value, chat_id),
            )
            conn.commit()

        return bool(new_value)

    def toggle_downloader(self, chat_id: int, downloader: str):
        with sqlite3.connect(self.db_path) as conn:
            self._ensure_chat_row(conn, chat_id)
            row = conn.execute(
                """
                SELECT 1
                FROM disabled_downloaders
                WHERE chat_id = ? AND downloader = ?
                """,
                (chat_id, downloader),
            ).fetchone()

            if row:
                conn.execute(
                    """
                    DELETE FROM disabled_downloaders
                    WHERE chat_id = ? AND downloader = ?
                    """,
                    (chat_id, downloader),
                )
                conn.commit()
                return False

            conn.execute(
                """
                INSERT INTO disabled_downloaders(chat_id, downloader)
                VALUES (?, ?)
                """,
                (chat_id, downloader),
            )
            conn.commit()
            return True
