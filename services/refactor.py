import os
import re
import requests
from dotenv import load_dotenv
from services.downloader_manager import DownloaderManager
from services.downloaders.query import QueryDownloader
from services.metadata_manger import MetadataManager
from services.metadata.metadata_writer import MetadataWriter
from services.metadata.spotify_metadata_provider import SpotifyMetadataProvider
from services.metadata.youtube_metadata_provider import YoutubeMetadataProvider
from services.spotify_auth import get_token
from services.downloaders.spotify import SpotifyDownloader
from services.downloaders.youtube import YouTubeDownloader
from services.metadata.song_id import SongIDService
from PIL import Image
from io import BytesIO
from pathlib import Path

load_dotenv()

def download_song(song_name: str) -> str | None:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    token = get_token(client_id, client_secret)

    spotify_metadata_provider = SpotifyMetadataProvider(token)
    youtube_metadata_provider = YoutubeMetadataProvider()

    project_root = Path(__file__).parent.parent.resolve()
    youtube_downloader = YouTubeDownloader(project_root)
    query_downloader = QueryDownloader(youtube_downloader)
    spotify_downloader = SpotifyDownloader(spotify_metadata_provider, query_downloader)
    url_downloaders = [spotify_downloader, youtube_downloader]
    searchable_downloaders = [query_downloader]
    manager = DownloaderManager(url_downloaders, searchable_downloaders)

    try:
        path = manager.download(song_name)
    except Exception as e:
        return str(e)

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

    metadata_writer = MetadataWriter()
    metadata_manager = MetadataManager([spotify_metadata_provider, youtube_metadata_provider], metadata_writer)

    metadata = metadata_manager.get_metadata(track_id if track_id else song_name)
    album_art_response = requests.get(metadata["thumbnail"])
    album_art = album_art_response.content

    album_art_img = Image.open(BytesIO(album_art)).convert("RGB")
    album_art_path = os.path.splitext(path)[0] + "_cover.jpg"
    album_art_img.save(album_art_path, format="JPEG")

    metadata_manager.write_metadata(path, metadata)
    metadata_manager.write_album_art(path, album_art_path)

    return path

download_song("")