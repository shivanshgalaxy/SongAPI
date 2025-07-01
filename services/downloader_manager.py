from typing import List, Union
from services.interfaces.downloader import UrlDownloader, SearchableDownloader
from utils.validation_utils import is_url


class DownloaderManager:
    def __init__(self, url_downloaders: List[UrlDownloader], searchable_downloaders: List[SearchableDownloader]):
        self.url_downloaders = url_downloaders
        self.searchable_downloaders = searchable_downloaders

    def download_track(self, query: str) -> str:
        if is_url(query):
            for downloader in self.url_downloaders:
                if downloader.can_handle(query):
                    return downloader.download_track(query)
            raise ValueError("No suitable URL downloader found")
        else:
            for downloader in self.searchable_downloaders:
                if downloader.can_handle(query):
                    return downloader.download_track(query)
            raise ValueError("No suitable query found")

    def download(self, query: str) -> Union[str, List[str]]:
        if is_url(query):
            for downloader in self.url_downloaders:
                if downloader.can_handle(query):
                    url_type = downloader.get_type(query)
                    if url_type == 'playlist':
                        track_urls = downloader.extract_track_from_playlist(query)
                        paths = []
                        for track_url in track_urls:
                            # For Spotify, track_url may be an ID, so reconstruct the URL
                            if 'spotify' in query and not track_url.startswith('http'):
                                track_url = f'https://open.spotify.com/track/{track_url}'
                            paths.append(self.download_track(track_url))
                        return paths
                    elif url_type == 'track':
                        return self.download_track(query)
            raise ValueError("No suitable URL downloader found")
        else:
            return self.download_track(query)
