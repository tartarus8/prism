import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token (Required for running the bot)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Yandex Music Token (Optional, public links can be fetched anonymously)
YANDEX_MUSIC_TOKEN = os.getenv("YANDEX_MUSIC_TOKEN")

# Mock file size in MB for Qobuz Downloader (Defaults to 15.0 MB)
# Set to > 50.0 to test Telegram's upload limit warning
try:
    MOCK_FILE_SIZE_MB = float(os.getenv("MOCK_FILE_SIZE_MB", "15.0"))
except ValueError:
    MOCK_FILE_SIZE_MB = 15.0

# Directory to save downloaded tracks
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
