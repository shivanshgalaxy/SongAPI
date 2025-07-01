from services.interfaces.metadata_providers import MetadataProvider
from services.metadata.metadata_writer import MetadataWriter
from utils.validation_utils import is_url
import sys


class MetadataManager(MetadataProvider):
    def __init__(self, providers: list[MetadataProvider], writer: MetadataWriter):
        self.providers = providers
        self.writer = writer

    def get_metadata(self, source: str | dict) -> dict:
        is_search_query = isinstance(source, str) and not is_url(source)

        for provider in self.providers:
            try:
                if is_search_query and hasattr(provider, "get_metadata_by_search"):
                    metadata = provider.get_metadata_by_search(source)
                else:
                    metadata = provider.get_metadata(source)

                if metadata:
                    print(f"{provider.__class__.__name__} provided metadata")
                    return metadata
            except Exception as e:
                print(f"Provider {provider.__class__.__name__} failed: {e}", file=sys.stderr)
                return {}
        return {}

    def write_metadata(self, filepath: str, metadata: dict) -> None:
        self.writer.write_metadata(filepath, metadata)

    def write_album_art(self, filepath: str, image_path: str) -> None:
        self.writer.write_album_art(filepath, image_path)