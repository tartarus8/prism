import os
from pathlib import Path


def get_file_size_mb(path: Path) -> float:
    """Returns the size of the file in Megabytes."""
    if not path.exists():
        return 0.0
    return os.path.getsize(path) / (1024 * 1024)


def safe_delete_file(path: Path) -> None:
    """Safely deletes a file from disk, swallowing exceptions."""
    try:
        if path.exists():
            path.unlink()
    except Exception:
        pass
