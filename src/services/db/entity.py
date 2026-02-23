import sqlite3
from dataclasses import dataclass

@dataclass
class ChatSettings:
    chat_id: int
    memes_enabled: bool
    disabled_downloaders: set[str]
