import sys
from services.interfaces.metadata_providers_interface import MetadataProvider
from requests import get

class SpotifyMetadataProvider(MetadataProvider):
    def __init__(self, token: str):
        self.token = token
        self.URL = "https://api.spotify.com/v1"

    def get_metadata(self, query: str) -> dict:
        query_url = f"{self.URL}/tracks/{query}"
        print(query_url)
        response = get(query_url, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code != 200:
            print(f"Spotify request failed: {response.status_code}", file=sys.stderr)
            return {}
        response_json = response.json()
        metadata = {
            "title": response_json.get("name"),
            "artist": response_json.get("artists")[0].get("name"),
            "thumbnail": response_json.get("album").get("images")[0].get("url"),
            "album": response_json.get("album").get("name"),
        }

        return metadata