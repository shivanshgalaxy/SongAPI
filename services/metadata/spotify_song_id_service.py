from requests import get

class SpotifySearchService:
    def __init__(self, token: str):
        self.token = token
        self.URL = "https://api.spotify.com/v1/search"

    def search_track_id(self, track: str, artist: str) -> str:
        params = {
            "q": f"track:{track} artist:{artist}",
            "type": "track",
            "limit": 1
        }
        response = get(self.URL, headers={"Authorization": f"Bearer {self.token}"}, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to search Spotify. Response code {response.status_code}")
        items = response.json().get("tracks", {}).get("items", [])
        if not items:
            raise Exception("No tracks found for query.")
        return items[0]["id"]