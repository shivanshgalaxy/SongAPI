import re
import os
from dotenv import load_dotenv
from services.spotify_auth import get_token
from services.interfaces.downloader_interfaces import UrlDownloader

load_dotenv()

class SpotifyDownloader(UrlDownloader):
    def can_handle(self, url: str) -> bool:
        return re.match(r"^https?://open\.spotify\.com/", url) is not None

    def download_track(self, url: str) -> str:
        token = get_token(os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET"))
        print(f"Downloading Spotify song: {url}")
        # download logic...

        return f"spotify_{url[-10:]}.mp3"

    def get_type(self, url: str) -> str:
        pass

    def extract_track_from_playlist(self, url: str) -> list[str]:
        pass