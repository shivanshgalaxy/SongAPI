import yt_dlp
from ytmusicapi import YTMusic

from services.interfaces.metadata_providers_interface import MetadataProvider
import sys


class YoutubeMetadataProvider(MetadataProvider):
    def __init__(self, ydl_options: dict = None):
        self.ydl_options = ydl_options or {"extract_flat": True ,"quiet": False}
        self.ytmusic = YTMusic()

    def get_metadata(self, video_id: str) -> dict:
        try:
            with yt_dlp.YoutubeDL(self.ydl_options) as ydl:
                info = ydl.extract_info(video_id, download=False)
                return {
                    "title": info.get("title"),
                    "artist": info.get("artists")[0],
                    "thumbnail": info.get("thumbnail"),
                    "album": info.get("album")
                }
        except Exception as e:
            print(f"Error in YoutubeMetadataProvider: {e}", file=sys.stderr)
            return {}

    def get_metadata_by_search(self, query: str) -> dict:
        try:
            results = self.ytmusic.search(query, filter="songs", limit=1)
            if not results:
                print(f"No results found for query: {query}", file=sys.stderr)
                return {}

            video_id = results[0]["videoId"]
            return self.get_metadata(video_id)
        except Exception as e:
            print(f"Search error: {e}", file=sys.stderr)
            return {}
