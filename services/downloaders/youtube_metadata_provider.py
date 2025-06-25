import yt_dlp
from services.interfaces.metadata_providers_interface import MetadataProvider


class YoutubeMetadataProvider(MetadataProvider):
    def __init__(self, ydl_options: dict = None):
        self.ydl_options = ydl_options or {"quiet": True}

    def get_metadata(self, video_id):
        with yt_dlp.YoutubeDL(self.ydl_options) as ydl:
            info = ydl.extract_info(video_id, download=False)
            return {
                "title": info.get("title"),
                "artist": info.get("uploader"),
                "thumbnail": info.get("thumbnail"),
            }