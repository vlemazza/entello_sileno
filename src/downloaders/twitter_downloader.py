import asyncio
from pathlib import Path
from gallery_dl import config
from gallery_dl.extractor import find
from gallery_dl.job import DownloadJob
from downloaders.media_downloader import MediaDownloader
from models.download_result import DownloadResult, MediaItem



class TwitterDownloader(MediaDownloader):

    IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
    VIDEO_EXT = {".mp4", ".webm"}

    def __init__(self):
        super().__init__()

    async def fetch_post(self, url):
        config.set(("extractor", "twitter"), "text-tweets", True)
        config.set(("postprocessor",), "metadata", True)
        config.set(("metadata",), "event", "post")
        config.set(("metadata",), "filename", "{tweet_id}")

        extractor = find(url)
        extractor.initialize()


        items = await asyncio.to_thread(lambda: list(extractor.items()))

        content = ""
        user = "Unknown"
        media = False

        if items:
            data = items[0][2]
            content = data.get("content") or data.get("full_text") or data.get("text") or ""
            author_data = data.get("author") or {}
            user = (
                author_data.get("nick")
                or author_data.get("name")
                or author_data.get("username")
                or "Unknown"
            )
            media = True
        else:
            try:
                user = extractor.user.title()
            except Exception:
                user = "Unknown"
            tweets = await asyncio.to_thread(lambda: list(extractor.tweets()))
            content = await self.search_metadata(tweets, "full_text") or ""

        return DownloadResult(
            content=content,
            user=user,
            has_media=media,
        )


    async def fetch_media(self, url):
        self.reset_temp_dir()
        media_files = []

        config.set(("extractor", "twitter"), "directory", "")
        config.set(("extractor", "twitter"), "base-directory", self.temp_dir)

        extractor = find(url)
        extractor.initialize()

        job = DownloadJob(url)
        await asyncio.to_thread(job.run)

        for path in sorted(Path(self.temp_dir).rglob("*"), key=lambda item: str(item)):
            if not path.is_file():
                continue

            ext = path.suffix.lower()

            if ext in self.IMAGE_EXT:
                media_type = "image"
            elif ext in self.VIDEO_EXT:
                media_type = "video"
                path = await self.finalize_video(str(path))

            else:
                continue

            media_files.append({
                "file_path": str(path),
                "type": media_type,
            })

        return DownloadResult(
            media=[MediaItem(file_path=m["file_path"], type=m["type"]) for m in media_files]
        )

    async def search_metadata(self, data, search):
        if isinstance(data, dict):
            for k, v in data.items():
                if k == search:
                    return v
                res = await self.search_metadata(v, search)
                if res is not None:
                    return res
        elif isinstance(data, list):
            for item in data:
                res = await self.search_metadata(item, search)
                if res is not None:
                    return res
        return None
