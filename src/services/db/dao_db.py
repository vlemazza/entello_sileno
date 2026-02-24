from services.db.repository import Repository

SUPPORTED_DOWNLOADERS = (
    "youtube",
    "instagram",
    "tiktok",
    "reddit",
    "twitter",
    "bluesky",
    "facebook",
    "generic",
)

_repository = Repository()


def get_chat_settings(chat_id: int):
    return _repository.get_chat_settings(chat_id)


def toggle_memes(chat_id: int):
    return _repository.toggle_memes(chat_id)


def toggle_downloader(chat_id: int, downloader: str):
    if downloader not in SUPPORTED_DOWNLOADERS:
        raise ValueError(f"Unsupported downloader: {downloader}")
    return _repository.toggle_downloader(chat_id, downloader)


def is_downloader_disabled(chat_id: int, downloader: str):
    if downloader not in SUPPORTED_DOWNLOADERS:
        return False
    settings = _repository.get_chat_settings(chat_id)
    return downloader in settings.disabled_downloaders
