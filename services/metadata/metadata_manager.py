from interfaces.metadata_providers_interface import MetadataProvider

class MetadataManager(MetadataProvider):
    def __init__(self, providers: list[MetadataProvider]):
        self.providers = providers

    def get_metadata(self, source: str) -> dict:
        for provider in self.providers:
            metadata = provider.get_metadata(source)
            if metadata:
                return metadata
        raise Exception("Failed to retrieve metadata from all providers.")
