import re
import yt_dlp
from requests import get
import sys

class SongIDService:
    def __init__(self, token: str):
        self.token = token
        self.URL = "https://api.spotify.com/v1/search"

    @staticmethod
    def extract_spotify_track_id(url: str) -> str | None:
        match = re.match(r"spotify\.com/(?:track|album|playlist|artist)/([a-zA-Z0-9]+)", url)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def extract_youtube_title(url: str) -> str | None:
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get("title")
        except Exception:
            return None

    def get_spotify_track_id(self, query: str) -> str | None:
        params = {
            "q": query,
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
