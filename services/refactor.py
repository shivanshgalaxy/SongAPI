import os
from dotenv import load_dotenv

from services.downloader_manager import DownloaderManager
from services.interfaces.downloader_interfaces import SearchableDownloader
from spotify_auth import get_token
from utils.url_utils import is_valid_url
from services.downloaders.spotify_downloader import SpotifyDownloader
from services.downloaders.youtube_downloader import YouTubeDownloader


load_dotenv()
def download_song(song_name: str) -> str | None:
    url_downloaders = [SpotifyDownloader(), YouTubeDownloader()]
    searchable_downloaders = [SearchableDownloader()]
    manager = DownloaderManager(url_downloaders, searchable_downloaders)
    try:
        path = manager.download(song_name)
        return path
    except Exception as e:
        return str(e)


def get_metadata(song_name: str):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise EnvironmentError("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your .env file.")

    token = get_token(client_id, client_secret)
    headers = {
        "Authorization": f"Bearer {token}"
    }

