import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.services.extractor_yandex import YandexMusicExtractor
from bot.core.exceptions import ExtractorError


def test_yandex_music_extractor_can_handle():
    extractor = YandexMusicExtractor()
    
    # Valid URLs
    assert extractor.can_handle("https://music.yandex.ru/album/1025555/track/9538356")
    assert extractor.can_handle("https://music.yandex.com/album/1025555/track/9538356")
    assert extractor.can_handle("https://music.yandex.ru/track/9538356")
    assert extractor.can_handle("https://music.yandex.by/album/123/track/456")
    
    # Invalid URLs
    assert not extractor.can_handle("https://music.yandex.ru/album/1025555")
    assert not extractor.can_handle("https://spotify.com/track/9538356")
    assert not extractor.can_handle("just some text")


@pytest.mark.asyncio
async def test_yandex_music_extractor_extract_metadata_success():
    extractor = YandexMusicExtractor()
    
    # Mocking ClientAsync and its response
    mock_client = AsyncMock()
    mock_track = MagicMock()
    mock_track.title = "Blinding Lights"
    mock_track.version = "Instrumental"
    
    mock_artist = MagicMock()
    mock_artist.name = "The Weeknd"
    mock_track.artists = [mock_artist]
    
    mock_album = MagicMock()
    mock_album.title = "After Hours"
    mock_album.year = 2020
    mock_track.albums = [mock_album]
    
    mock_track.duration_ms = 200000
    mock_track.cover_uri = "avatars.yandex.net/get-music-content/123/%%"
    
    mock_client.tracks.return_value = [mock_track]
    
    # Inject mock client getter
    extractor._get_client = AsyncMock(return_value=mock_client)
    
    metadata = await extractor.extract_metadata("https://music.yandex.ru/album/1025555/track/9538356")
    
    assert metadata.title == "Blinding Lights (Instrumental)"
    assert metadata.artists == ["The Weeknd"]
    assert metadata.album == "After Hours"
    assert metadata.release_year == 2020
    assert metadata.duration_ms == 200000
    assert metadata.cover_url == "https://avatars.yandex.net/get-music-content/123/400x400"
    
    
@pytest.mark.asyncio
async def test_yandex_music_extractor_extract_metadata_not_found():
    extractor = YandexMusicExtractor()
    mock_client = AsyncMock()
    mock_client.tracks.return_value = []  # Empty track list
    
    extractor._get_client = AsyncMock(return_value=mock_client)
    
    with pytest.raises(ExtractorError) as exc_info:
        await extractor.extract_metadata("https://music.yandex.ru/album/1025555/track/9538356")
    assert "not found" in str(exc_info.value)
