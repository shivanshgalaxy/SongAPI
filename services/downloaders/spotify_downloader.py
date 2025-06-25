import re
import os
from dotenv import load_dotenv

from services.interfaces.metadata_providers_interface import MetadataProvider
from services.interfaces.downloader_interfaces import UrlDownloader

load_dotenv()

class SpotifyDownloader(UrlDownloader):
    def __init__(self, metadata_provider: MetadataProvider):
        self.metadata_provider = metadata_provider

    def can_handle(self, url: str) -> bool:
        return re.match(r"^https?://open\.spotify\.com/", url) is not None

    def download_track(self, url: str) -> str:
        song_data = self.metadata_provider.get_metadata(url)
        return f"spotify_{url[-10:]}.mp3"

    def get_type(self, url: str) -> str:
        pass

    def extract_track_from_playlist(self, url: str) -> list[str]:
        pass