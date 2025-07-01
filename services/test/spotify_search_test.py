import os

from dotenv import load_dotenv

from services.metadata.metadata import MetadataManager
from services.metadata.metadata_writer import MetadataWriter
from services.metadata.spotify_metadata_provider import SpotifyMetadataProvider
from services.metadata.spotify_song_id import SpotifySearchService
from services.metadata.youtube_metadata_provider import YoutubeMetadataProvider
from services.spotify_auth import get_token
import json

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
token = get_token(client_id, client_secret)

# https://open.spotify.com/track/3zL0LAsSh3dTO73dSOKWkr?si=8bbf02d0b0c346ea

# youtube = YoutubeMetadataProvider()
# spotify = SpotifyMetadataProvider(token)
# writer = MetadataWriter()
# manager = MetadataManager([spotify, youtube], writer)
# metadata = manager.get_metadata("https://music.youtube.com/watch?v=8WuVWqyGPcs&si=OuAeaw6-il7Grllf")

spotify_id = SpotifySearchService(token)
print(spotify_id.search_track_id("let it be beatles"))
