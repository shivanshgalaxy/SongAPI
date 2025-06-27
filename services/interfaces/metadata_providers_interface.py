from abc import ABC, abstractmethod

class MetadataProvider(ABC):
    @abstractmethod
    def get_metadata(self, query: str) -> dict:
        """
        Given a URL or query, returns a metadata dict with fields like:
        - title
        - artist
        - album
        - thumbnail
        """
        pass
