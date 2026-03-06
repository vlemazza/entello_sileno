from services.db.repository import Repository

SUPPORTED_DOWNLOADERS = (
    "youtube",
    "instagram",
    "tiktok",
    "reddit",
    "twitter",
    "bluesky",
    "facebook",
    "threads",
    "vimeo",
    "generic",
)

_repository = Repository()


async def get_chat_settings(chat_id: int):
    return await _repository.get_chat_settings(chat_id)


async def toggle_memes(chat_id: int):
    return await _repository.toggle_memes(chat_id)


async def toggle_downloader(chat_id: int, downloader: str):
    if downloader not in SUPPORTED_DOWNLOADERS:
        raise ValueError(f"Unsupported downloader: {downloader}")
    return await _repository.toggle_downloader(chat_id, downloader)


async def is_downloader_disabled(chat_id: int, downloader: str):
    if downloader not in SUPPORTED_DOWNLOADERS:
        return False
    settings = await _repository.get_chat_settings(chat_id)
    return downloader in settings.disabled_downloaders
