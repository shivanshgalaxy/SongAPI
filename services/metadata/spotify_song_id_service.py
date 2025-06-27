from requests import get
import sys

class SpotifyFindTrackID:
    def __init__(self, token: str):
        self.token = token
        self.URL = "https://api.spotify.com/v1/search"

    def find_track_id(self, track: str = None, artist: str = None) -> str | None:
        params = {
            "q": f"track:{track} artist:{artist}",
            "type": "track",
            "limit": 1
        }
        response = get(self.URL, headers={"Authorization": f"Bearer {self.token}"}, params=params)
        if response.status_code != 200:
            print(f"Failed to search Spotify. Response code {response.status_code}", file=sys.stderr)
        items = response.json().get("tracks", {}).get("items", [])
        if not items:
            print("No tracks found for query.", file=sys.stderr)
            return None
        return items[0]["id"]