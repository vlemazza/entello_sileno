import os
import yt_dlp
from downloaders.video_downloader import VideoDownloader

class YouTubeDownloader(VideoDownloader):
    def __init__(self):
        super().__init__()
        self.max_duration = int(os.getenv("MAX_DURATION"))
    

    def download_video(self, url):
        self.reset_temp_dir()
        ydl_opts = {
            'format': 'bv*[vcodec^=avc1][height<=720]+ba/b[height<=720]',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(self.temp_dir, "video_original.%(ext)s"),
            'quiet': False,
            'noplaylist': True,
            'no_warnings': True,
            'restrictfilenames': True,
            'overwrites': True,
            'continuedl': False,
            
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
                }],
    
        }


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
            title = info.get('title', 'unknown')
            description = info.get('description', '')
            uploader = info.get('uploader', 'unknown')

            if duration > self.max_duration:
                raise ValueError("[YouTubeDownloader] video exceeds %s", self.max_duration)

            ydl.download([url])

        if not os.path.exists(self.original_path):
            raise FileNotFoundError("File non trovato dopo il download.")

        size_mb = os.path.getsize(self.original_path) / (1024 * 1024)
        final_path = self.original_path

        if size_mb > 50:
            self.compress_video(self.original_path, self.compressed_path)
            final_path = self.compressed_path

        return {
            "media": [{"file_path": final_path, "type": "video"}],
            "title": title,
            "description": description,
            "author": uploader,
        }

    def download_audio(self, url):
        self.reset_temp_dir()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.temp_dir, 'audio_original.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'overwrites': True,
            'writethumbnail': True,
            'addmetadata': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
            {
            'key': 'FFmpegMetadata',
            },
            {
            'key': 'EmbedThumbnail',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'unknown')
            duration = info.get('duration', 0)
            if duration > self.max_duration:
                raise ValueError(
                    f"[YouTubeDownloaderAudio] audio exceeds {self.max_duration}s"
                )

        audio_path = os.path.join(self.temp_dir, "audio_original.mp3")

        if not os.path.exists(audio_path):
            raise FileNotFoundError("Audio non trovato dopo il download.")

        new_audio_path = os.path.join(self.temp_dir, f"{title}.mp3")
        os.rename(audio_path, new_audio_path)

        return {
            "media": [{"file_path": new_audio_path, "type": "audio"}],
            "title": title,
            "description": "",
            "author": "",
        }
