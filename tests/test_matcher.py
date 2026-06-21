import pytest
from bot.core.models import TrackMetadata
from bot.services.matcher_heuristic import HeuristicMatcher


@pytest.mark.asyncio
async def test_heuristic_matcher_basic():
    matcher = HeuristicMatcher()
    metadata = TrackMetadata(
        title="Yesterday",
        artists=["The Beatles"],
        album="Help!",
        release_year=1965,
        duration_ms=125000,
        original_url="https://music.yandex.ru/track/123"
    )
    query = await matcher.match(metadata)
    assert query == "The Beatles - Yesterday"


@pytest.mark.asyncio
async def test_heuristic_matcher_multiple_artists_and_album():
    matcher = HeuristicMatcher(include_album=True)
    metadata = TrackMetadata(
        title="Harder, Better, Faster, Stronger",
        artists=["Daft Punk", "Daft Guest"],
        album="Discovery",
        release_year=2001,
        duration_ms=224000,
        original_url="https://music.yandex.ru/track/456"
    )
    query = await matcher.match(metadata)
    assert query == "Daft Punk Daft Guest - Harder, Better, Faster, Stronger Discovery"
