import re
from utils.validation_utils import sanitize_filename
from services.interfaces.downloader import UrlDownloader
import yt_dlp
import os


class YouTubeDownloader(UrlDownloader):
    def __init__(self, download_dir):
        self.download_dir = download_dir

    def can_handle(self, url: str) -> bool:
        return re.match(r"^https?://(www\.)?(youtube\.com|youtu\.be)", url) is not None

    def download_track(self, url: str) -> str:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "audio")
        output_path = os.path.join(self.download_dir, f'{sanitize_filename(title)}.mp3')
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': os.path.join(self.download_dir, f'{sanitize_filename(title)}.%(ext)s') ,  # Output file name template
            'quiet': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return output_path

    def get_type(self, url: str) -> str:
        if 'playlist' in url or 'list=' in url:
            return "playlist"
        elif re.match(r"https?://(www\.)?(youtube\.com|youtu\.be)/watch", url):
            return "track"
        else:
            return "unknown"

    def extract_track_from_playlist(self, url: str) -> list[str]:
        ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            entries = info.get('entries', [])
            video_urls = []
            for entry in entries:
                if 'url' in entry:
                    video_urls.append(f"https://www.youtube.com/watch?v={entry['url']}")
                elif 'id' in entry:
                    video_urls.append(f"https://www.youtube.com/watch?v={entry['id']}")
            return video_urls