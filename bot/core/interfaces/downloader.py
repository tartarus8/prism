from abc import ABC, abstractmethod
from pathlib import Path
from bot.core.models import TrackMetadata


class BaseAudioDownloader(ABC):
    @abstractmethod
    async def download(self, query: str, metadata: TrackMetadata) -> Path:
        """
        Asynchronously searches and downloads the track.
        Returns a Path object pointing to the downloaded FLAC/MP3 file.
        """
        pass
