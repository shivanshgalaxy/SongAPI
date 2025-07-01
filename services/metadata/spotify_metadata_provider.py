import sys
from services.interfaces.metadata_providers import MetadataProvider
from requests import get
from services.metadata.spotify_song_id import SongIDService

class SpotifyMetadataProvider(MetadataProvider):
    def __init__(self, token: str):
        self.token = token
        self.URL = "https://api.spotify.com/v1"

    def get_metadata(self, track_id: str) -> dict:
        query_url = f"{self.URL}/tracks/{track_id}"
        response = get(query_url, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code != 200:
            print(f"Spotify request failed: {response.status_code}", file=sys.stderr)
            return {}
        response_json = response.json()
        return {
            "title": response_json.get("name"),
            "artist": response_json.get("artists")[0].get("name"),
            "thumbnail": response_json.get("album").get("images")[0].get("url"),
            "album": response_json.get("album").get("name"),
        }
