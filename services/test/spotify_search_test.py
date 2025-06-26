import os

from dotenv import load_dotenv

from services.metadata.spotify_song_id_service import SpotifySearchService
from services.spotify_auth import get_token

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
token = get_token(client_id, client_secret)
search = SpotifySearchService(token)
print(search.search_track_id("sapphire", "ed sheeran"))


