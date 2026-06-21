import pytest
from pathlib import Path
from bot.core.models import TrackMetadata
from bot.services.downloader_qobuz import QobuzDownloader
from bot.utils.helpers import get_file_size_mb, safe_delete_file


@pytest.mark.asyncio
async def test_qobuz_downloader_creates_file():
    download_dir = "test_downloads"
    downloader = QobuzDownloader(download_dir=download_dir, mock_file_size_mb=2.0)
    
    metadata = TrackMetadata(
        title="Yesterday",
        artists=["The Beatles"],
        album="Help!",
        release_year=1965,
        duration_ms=125000,
        original_url="https://music.yandex.ru/track/123"
    )
    
    file_path = await downloader.download("The Beatles - Yesterday", metadata)
    
    assert isinstance(file_path, Path)
    assert file_path.exists()
    assert file_path.suffix == ".flac"
    
    # Check that our custom FLAC magic header is intact
    with open(file_path, "rb") as f:
        header = f.read(4)
        assert header == b"fLaC"
        
    size_mb = get_file_size_mb(file_path)
    # Due to sparse files and block allocation, check size within reasonable delta
    assert abs(size_mb - 2.0) < 0.01
    
    # Clean up the file
    safe_delete_file(file_path)
    
    # Clean up the directory if empty
    test_dir_path = Path(download_dir)
    if test_dir_path.exists():
        try:
            test_dir_path.rmdir()
        except OSError:
            pass
