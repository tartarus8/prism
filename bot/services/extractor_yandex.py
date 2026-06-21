import re
from typing import Optional
from yandex_music import ClientAsync

from bot.core.interfaces.extractor import BaseMetadataExtractor
from bot.core.models import TrackMetadata
from bot.core.exceptions import ExtractorError


class YandexMusicExtractor(BaseMetadataExtractor):
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self._client: Optional[ClientAsync] = None
        self._track_re = re.compile(
            r'music\.yandex\.(?:ru|com|by|kz|ua)/(?:album/\d+/)?track/(\d+)'
        )

    async def _get_client(self) -> ClientAsync:
        if self._client is None:
            self._client = ClientAsync(token=self.token)
            await self._client.init()
        return self._client

    def can_handle(self, url: str) -> bool:
        return bool(self._track_re.search(url))

    async def extract_metadata(self, url: str) -> TrackMetadata:
        match = self._track_re.search(url)
        if not match:
            raise ExtractorError(f"Invalid Yandex Music URL: {url}")

        track_id = match.group(1)
        try:
            client = await self._get_client()
            tracks = await client.tracks([track_id])
            if not tracks:
                raise ExtractorError(f"Track with ID {track_id} not found.")

            track = tracks[0]
            
            # Format title (include version if available)
            title = track.title
            if getattr(track, 'version', None):
                title = f"{title} ({track.version})"

            # Extract artists
            artists = []
            if getattr(track, 'artists', None):
                artists = [artist.name for artist in track.artists if getattr(artist, 'name', None)]
            if not artists:
                artists = ["Unknown Artist"]

            # Extract album info
            album_title = None
            release_year = None
            if getattr(track, 'albums', None) and len(track.albums) > 0:
                album = track.albums[0]
                album_title = getattr(album, 'title', None)
                if getattr(album, 'year', None):
                    release_year = album.year
                elif getattr(album, 'release_date', None):
                    try:
                        if hasattr(album.release_date, 'year'):
                            release_year = album.release_date.year
                        else:
                            release_year = int(str(album.release_date).split('-')[0])
                    except Exception:
                        pass

            # Cover URL
            cover_url = None
            if getattr(track, 'cover_uri', None):
                cover_url = "https://" + track.cover_uri.replace("%%", "400x400")

            return TrackMetadata(
                title=title,
                artists=artists,
                album=album_title,
                release_year=release_year,
                duration_ms=getattr(track, 'duration_ms', None),
                cover_url=cover_url,
                original_url=url
            )
        except Exception as e:
            raise ExtractorError(f"Failed to extract metadata from Yandex Music: {e}") from e
