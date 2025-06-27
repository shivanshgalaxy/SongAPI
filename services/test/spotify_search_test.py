import os

from dotenv import load_dotenv

from services.metadata.metadata_manager import MetadataManager
from services.metadata.metadata_writer import MetadataWriter
from services.metadata.spotify_metadata_provider import SpotifyMetadataProvider
from services.metadata.youtube_metadata_provider import YoutubeMetadataProvider
from services.spotify_auth import get_token
import json

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
token = get_token(client_id, client_secret)


