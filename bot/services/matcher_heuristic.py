import re
from bot.core.interfaces.matcher import BaseMatcher
from bot.core.models import TrackMetadata


class HeuristicMatcher(BaseMatcher):
    """
    A basic string-matching heuristic matcher.
    To plug in an LLM (like OpenAI or Gemini) later, you can create a new class:
    
    class LLMMatcher(BaseMatcher):
        async def match(self, metadata: TrackMetadata) -> str:
            # Call OpenAI/Gemini API here to translate, clean up, and match names
            ...
    """

    def __init__(self, include_album: bool = False):
        self.include_album = include_album

    async def match(self, metadata: TrackMetadata) -> str:
        """
        Builds a highly accurate search query by cleaning and formatting the metadata.
        """
        # Clean artists and join them
        artists_clean = [artist.strip() for artist in metadata.artists if artist.strip()]
        artists_str = " ".join(artists_clean)

        # Clean track title
        title_clean = metadata.title.strip()

        # Construct search query
        query = f"{artists_str} - {title_clean}"

        # Optionally append album for additional search precision
        if self.include_album and metadata.album:
            album_clean = metadata.album.strip()
            if album_clean and album_clean.lower() not in title_clean.lower():
                query += f" {album_clean}"

        # Remove any redundant whitespaces
        query = re.sub(r'\s+', ' ', query).strip()

        return query
