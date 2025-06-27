import sys
from services.interfaces.metadata_providers_interface import MetadataProvider
from requests import get
from services.metadata.spotify_song_id_service import SpotifyFindTrackID
from utils.validation_utils import is_url, extract_spotify_id


class SpotifyMetadataProvider(MetadataProvider):
    def __init__(self, token: str, search_service: SpotifyFindTrackID):
        self.token = token
        self.URL = "https://api.spotify.com/v1"
        self.search_service = search_service

    def get_metadata(self, query: str | dict) -> dict:
        # If a Spotify track ID is passed directly
        if is_url(query):
            query = extract_spotify_id(query)

        if isinstance(query, str) and len(query) == 22:  # Spotify track IDs are 22 chars
            track_id = query
        # If dict like {"title": ..., "artist": ...}
        elif isinstance(query, dict):
            title = query.get("title")
            artist = query.get("artist")
            if not title and not artist:
                print("Missing title and artist for Spotify search", file=sys.stderr)
                return {}
            track_id = self.search_service.find_track_id(title, artist)
            if not track_id:
                print(f"Could not find Spotify track ID for {title} by {artist}", file=sys.stderr)
                return {}
        else:
            print("Invalid query type for SpotifyMetadataProvider", file=sys.stderr)
            return {}

        # Fetch metadata from Spotify
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
