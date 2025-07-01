from abc import ABC, abstractmethod

class UrlDownloader(ABC):
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        pass

    @abstractmethod
    def download_track(self, url: str) -> str:
        pass

    @abstractmethod
    def get_type(self, url: str) -> str:
        pass

    @abstractmethod
    def extract_track_from_playlist(self, url: str) -> list[str]:
        pass


class SearchableDownloader(ABC):
    @abstractmethod
    def can_handle(self, query: str) -> bool:
        pass
    @abstractmethod
    def download_track(self, query: str) -> str:
        pass
