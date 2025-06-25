from typing import List
from services.interfaces.downloader_interfaces import UrlDownloader, SearchableDownloader
from utils.validation_utils import is_valid_url


class DownloaderManager:
    def __init__(self, url_downloaders: List[UrlDownloader], searchable_downloaders: List[SearchableDownloader]):
        self.url_downloaders = url_downloaders
        self.searchable_downloaders = searchable_downloaders

    def download(self, query: str) -> str:
        if is_valid_url(query):
            for downloader in self.url_downloaders:
                if downloader.can_handle(query):
                    return downloader.download_track(query)
            raise ValueError("No suitable URL downloader found")
        else:
            for downloader in self.searchable_downloaders:
                if downloader.can_handle(query):
                    return downloader.download_track(query)
            raise ValueError("No suitable query found")

