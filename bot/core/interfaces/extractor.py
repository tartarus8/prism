from abc import ABC, abstractmethod
from bot.core.models import TrackMetadata


class BaseMetadataExtractor(ABC):
    @abstractmethod
    async def extract_metadata(self, url: str) -> TrackMetadata:
        """
        Asynchronously parses the music platform URL
        and returns a structured TrackMetadata model.
        """
        pass

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Checks if the given URL can be parsed by this extractor."""
        pass
