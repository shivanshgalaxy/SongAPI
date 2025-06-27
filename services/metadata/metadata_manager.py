from services.interfaces.metadata_providers_interface import MetadataProvider
from services.metadata.metadata_writer import MetadataWriter


class MetadataManager(MetadataProvider):
    def __init__(self, providers: list[MetadataProvider], writer: MetadataWriter):
        self.providers = providers
        self.writer = writer

    def get_metadata(self, source: str) -> dict:
        for provider in self.providers:
            metadata = provider.get_metadata(source)
            if metadata:
                print(provider)
                return metadata
        raise Exception("Failed to retrieve metadata from all providers.")

    def write_metadata(self, filepath: str, metadata: dict) -> None:
        self.writer.write_metadata(filepath, metadata)

    def write_album_art(self, filepath: str, image_path: str) -> None:
        self.writer.write_album_art(filepath, image_path)