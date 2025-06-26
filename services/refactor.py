import os
from dotenv import load_dotenv
from services.downloader_manager import DownloaderManager
from services.downloaders.query_downloader import QueryDownloader
from services.metadata.spotify_metadata_provider import SpotifyMetadataProvider
from services.spotify_auth import get_token
from services.downloaders.spotify_downloader import SpotifyDownloader
from services.downloaders.youtube_downloader import YouTubeDownloader


load_dotenv()
def download_song(song_name: str) -> str | None:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    token = get_token(client_id, client_secret)
    spotify_metadata_provider = SpotifyMetadataProvider(token)
    youtube_downloader = YouTubeDownloader()
    query_downloader = QueryDownloader(youtube_downloader)
    spotify_downloader = SpotifyDownloader(spotify_metadata_provider, query_downloader)

    url_downloaders = [spotify_downloader, youtube_downloader]
    searchable_downloaders = [query_downloader]
    manager = DownloaderManager(url_downloaders, searchable_downloaders)
    try:
        path = manager.download(song_name)
    except Exception as e:
        return str(e)


    return path