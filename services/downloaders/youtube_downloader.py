import re
from services.interfaces.downloader_interfaces import UrlDownloader
import yt_dlp

class YouTubeDownloader(UrlDownloader):
    def can_handle(self, url: str) -> bool:
        return re.match(r"^https?://(www\.)?(youtube\.com|youtu\.be)", url) is not None

    def download_track(self, url: str) -> str:
        print(f"Downloading YouTube video: {url}")
        # download logic...
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',  # Output file name template
            'quiet': False,  # Set to True to suppress output
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return f"youtube_{url[-10:]}.mp4"
