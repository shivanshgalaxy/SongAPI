import re
from dotenv import load_dotenv
import json
from services.interfaces.metadata_providers import MetadataProvider
from services.interfaces.downloader import UrlDownloader, SearchableDownloader
from services.metadata.spotify_song_id import SongIDService

load_dotenv()

class SpotifyDownloader(UrlDownloader):
    def __init__(self, metadata_provider: MetadataProvider, query_downloader: SearchableDownloader):
        self.query_downloader = query_downloader
        self.metadata_provider = metadata_provider

    def can_handle(self, url: str) -> bool:
        return re.match(r"^https?://open\.spotify\.com/", url) is not None

    def download_track(self, url: str) -> str:
        song_id = SongIDService.extract_spotify_track_id(url)
        song_data = self.metadata_provider.get_metadata(song_id)
        song_artist = song_data["artist"]
        song_title = song_data["title"]
        return self.query_downloader.download_track(f"{song_artist} {song_title}")

    def get_type(self, url: str) -> str:
        pass

    def extract_track_from_playlist(self, url: str) -> list[str]:
        pass