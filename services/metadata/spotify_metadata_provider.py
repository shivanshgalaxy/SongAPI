from services.interfaces.metadata_providers_interface import MetadataProvider
from requests import get


class SpotifyMetadataProvider(MetadataProvider):
    def __init__(self, token: str):
        self.token = token
        self.URL = "https://api.spotify.com/v1/"

    def get_metadata(self, api_endpoint: str, query: str) -> dict:
        query_url = f"{self.URL}{api_endpoint}/{query}"
        print(query_url)
        response = get(query_url, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code != 200:
            raise Exception("Failed to retrieve metadata from Spotify.")
        return response.json()