import re
from dotenv import load_dotenv
import json
from services.interfaces.metadata_providers import MetadataProvider
from services.interfaces.downloader import UrlDownloader, SearchableDownloader
from services.metadata.spotify_song_id import SongIDService
import requests

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
        if re.match(r"https?://open\.spotify\.com/track/", url):
            return "track"
        elif re.match(r"https?://open\.spotify\.com/playlist/", url):
            return "playlist"
        else:
            return "unknown"

    def extract_track_from_playlist(self, url: str) -> list[str]:
        playlist_id_match = re.match(r"https?://open\.spotify\.com/playlist/([a-zA-Z0-9]+)", url)
        if not playlist_id_match:
            return []
        playlist_id = playlist_id_match.group(1)
        token = self.metadata_provider.token if hasattr(self.metadata_provider, 'token') else None
        if not token:
            raise ValueError("Spotify API token required for playlist extraction.")
        headers = {"Authorization": f"Bearer {token}"}
        tracks = []
        offset = 0
        while True:
            api_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit=100"
            resp = requests.get(api_url, headers=headers)
            if resp.status_code != 200:
                break
            data = resp.json()
            items = data.get("items", [])
            for item in items:
                track = item.get("track")
                if track and track.get("id"):
                    tracks.append(track["id"])
            if not data.get("next"):
                break
            offset += 100
        return tracks

