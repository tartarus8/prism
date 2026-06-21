from abc import ABC, abstractmethod
from bot.core.models import TrackMetadata


class BaseMatcher(ABC):
    @abstractmethod
    async def match(self, metadata: TrackMetadata) -> str:
        """
        Processes TrackMetadata and formats/returns a highly accurate query string
        or ID optimized for searching on the target high-res platform.
        """
        pass
