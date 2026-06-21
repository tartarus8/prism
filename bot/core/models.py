from pydantic import BaseModel
from typing import Optional, List


class TrackMetadata(BaseModel):
    title: str
    artists: List[str]
    album: Optional[str] = None
    release_year: Optional[int] = None
    duration_ms: Optional[int] = None
    cover_url: Optional[str] = None
    original_url: str
