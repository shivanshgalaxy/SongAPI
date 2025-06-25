from services.interfaces.downloader_interfaces import SearchableDownloader, UrlDownloader
from ytmusicapi import YTMusic

class QueryDownloader(SearchableDownloader):
    def __init__(self, youtube_downloader: UrlDownloader):
        self.youtube_downloader = youtube_downloader

    def can_handle(self, query: str) -> bool:
        # Implement logic to determine if this downloader can handle the query
        return True  # Placeholder, should be replaced with actual logic

    def download_track(self, query: str) -> str:
        yt_music_api = YTMusic()
        search_results = yt_music_api.search(query, limit=1, filter="songs")
        video_id = search_results[0]["videoId"]
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        return self.youtube_downloader.download_track(youtube_url)