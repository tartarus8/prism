import asyncio
from pathlib import Path
from bot.core.models import TrackMetadata
from bot.core.interfaces.downloader import BaseAudioDownloader

class QobuzDownloader(BaseAudioDownloader):
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    async def download(self, query: str, metadata: TrackMetadata) -> Path:
        """
        Uses 'streamrip' via async subprocess to fetch the FLAC.
        We assume 'query' here is the Qobuz Track ID or a direct Qobuz URL.
        """
        # Example command: rip url "https://open.qobuz.com/track/1234567" --folder ./downloads
        command = [
            "rip", "url", 
            query, # Qobuz Track ID or URL passed from the Matcher
            "--folder", str(self.download_dir),
            "--quiet" # Prevent it from polluting your bot's terminal logs
        ]

        # Run the command asynchronously so the bot doesn't freeze
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"Failed to download from Qobuz: {stderr.decode()}")

        # Streamrip creates the file in the target directory.
        # We need to find the newly created .flac file.
        # (A more robust way is to read the exact filename from streamrip's stdout)
        downloaded_files = list(self.download_dir.glob("*.flac"))
        
        # Sort by creation time to get the newest one
        if not downloaded_files:
            raise Exception("Download succeeded but no FLAC file was found.")
            
        newest_file = max(downloaded_files, key=lambda f: f.stat().st_ctime)
        return newest_file