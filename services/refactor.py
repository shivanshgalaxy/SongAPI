import os
import re
from dotenv import load_dotenv
from services.downloader_manager import DownloaderManager
from services.downloaders.query import QueryDownloader
from services.metadata.metadata_manger import MetadataManager
from services.metadata.metadata_writer import MetadataWriter
from services.metadata.spotify_metadata_provider import SpotifyMetadataProvider
from services.spotify_auth import get_token
from services.downloaders.spotify import SpotifyDownloader
from services.downloaders.youtube import YouTubeDownloader
from services.metadata.spotify_song_id import SongIDService

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

    track_id = None
    song_id_service = SongIDService(token)
    if re.match(r"https?://open\.spotify\.com/track/", song_name):
        track_id = SongIDService.extract_spotify_track_id(song_name)
    elif re.match(r"https?://(www\.)?(youtube\.com|youtu\.be)", song_name):
        yt_title = SongIDService.extract_youtube_title(song_name)
        if yt_title:
            track_id = song_id_service.get_spotify_track_id(yt_title)
    else:
        track_id = song_id_service.get_spotify_track_id(song_name)

    try:
        path = manager.download(song_name)
    except Exception as e:
        return str(e)

    metadata_writer = MetadataWriter()
    metadata_manager = MetadataManager()
    
    return path



