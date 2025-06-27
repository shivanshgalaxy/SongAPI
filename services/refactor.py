import os
from dotenv import load_dotenv
from requests import get
from services.downloader_manager import DownloaderManager
from services.downloaders.query_downloader import QueryDownloader
from services.metadata.metadata_manager import MetadataManager
from services.metadata.metadata_writer import MetadataWriter
from services.metadata.spotify_metadata_provider import SpotifyMetadataProvider
from services.metadata.spotify_song_id_service import SpotifyFindTrackID
from services.metadata.youtube_metadata_provider import YoutubeMetadataProvider
from services.spotify_auth import get_token
from services.downloaders.spotify_downloader import SpotifyDownloader
from services.downloaders.youtube_downloader import YouTubeDownloader
from pathlib import Path
import json
from PIL import Image
from io import BytesIO


load_dotenv()
def download_song(song_name: str) -> str | None:
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    token = get_token(client_id, client_secret)
    spotify_find_track_id = SpotifyFindTrackID(token)
    spotify_metadata_provider = SpotifyMetadataProvider(token, spotify_find_track_id)
    youtube_downloader = YouTubeDownloader(Path("~/Projects/PythonProjects/SongAPI").expanduser())
    query_downloader = QueryDownloader(youtube_downloader)
    spotify_downloader = SpotifyDownloader(spotify_metadata_provider, query_downloader)
    url_downloaders = [spotify_downloader, youtube_downloader]
    searchable_downloaders = [query_downloader]
    manager = DownloaderManager(url_downloaders, searchable_downloaders)
    try:
        path = manager.download(song_name)
    except Exception as e:
        return str(e)

    youtube_metadata_provider = YoutubeMetadataProvider()
    metadata_writer = MetadataWriter()
    metadata_manager = MetadataManager([spotify_metadata_provider, youtube_metadata_provider], metadata_writer)
    metadata = metadata_manager.get_metadata(song_name)
    print(json.dumps(metadata, indent=2))
    album_art_url = metadata.get("thumbnail")
    album_art_data = get(album_art_url).content


    album_art_path = Path(f"~/Projects/PythonProjects/SongAPI/album_art.jpg").expanduser()
    if album_art_url:
        image = Image.open(BytesIO(album_art_data)).convert("RGB")
        image.save(album_art_path, "JPEG")
    else:
        print("No album art found for this song.")

    metadata_manager.write_metadata(path, metadata)
    metadata_manager.write_album_art(path, str(album_art_path))
    return path

download_song("https://open.spotify.com/track/7gHs73wELdeycvS48JfIos")