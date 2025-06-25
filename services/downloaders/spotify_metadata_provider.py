from services.interfaces.metadata_providers_interface import MetadataProvider
from requests import get


class SpotifyMetadataProvider(MetadataProvider):
    def __init__(self, token: str, endpoint: str, query: str):
        self.token = token
        self.URL = "https://api.spotify.com/v1/"
        self.endpoint = endpoint
        self.query = query

    def get_metadata(self, source: str) -> dict:
        query_url = f"{self.URL}{self.endpoint}/{self.query}"
        response = get(query_url, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code != 200:
            raise Exception("Failed to retrieve metadata from Spotify.")
        return response.json()