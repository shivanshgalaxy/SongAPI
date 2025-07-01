import re
from utils.validation_utils import sanitize_filename
from services.interfaces.downloader import UrlDownloader
import yt_dlp


class YouTubeDownloader(UrlDownloader):
    def can_handle(self, url: str) -> bool:
        return re.match(r"^https?://(www\.)?(youtube\.com|youtu\.be)", url) is not None

    def download_track(self, url: str) -> str:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "audio")
        print(sanitize_filename(title))
        print(f"Downloading YouTube video: {url}")
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': f'{sanitize_filename(title)}.%(ext)s',  # Output file name template
            'quiet': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return "Download completed for YouTube video: " + url

    def get_type(self, url: str) -> str:
        pass

    def extract_track_from_playlist(self, url: str) -> list[str]:
        pass