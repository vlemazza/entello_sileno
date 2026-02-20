import os
from pathlib import Path
from utils.logger import debug
from downloaders.video_downloader import VideoDownloader
from RedDownloader import RedDownloader

class RedditDownloader(VideoDownloader):
    def __init__(self):
        super().__init__()

    async def download_post(self, url):

        self.reset_temp_dir()
        media_files = []

        try:
            post = RedDownloader.Download(
                url,
                destination=os.path.join(self.temp_dir, "")
            )

            match post.GetMediaType():
                case "i":
                    type_post = "image"
                case "v":
                    type_post = "video"
                case "g":
                    type_post = "image"

        except Exception:
            debug("[RedditDownloader] fallback su video downodder generic")
            video = await self.download_video(url)
            return {
                "media": video["media"],
                "title": "",
                "description": "",
                "author": "",
            }
        

        for path_obj in sorted(Path(self.temp_dir).rglob("*"), key=lambda item: str(item)):
            if path_obj.is_file():
                media_files.append({
                    "file_path": str(path_obj),
                    "type": type_post,
                })

        return {
            "media": media_files,
            "title": RedDownloader.GetPostTitle(url).Get(),
            "description": "",
            "author": "",
        }
