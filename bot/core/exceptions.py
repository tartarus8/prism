class BotError(Exception):
    """Base exception for all bot errors."""
    pass


class ExtractorError(BotError):
    """Raised when metadata extraction fails."""
    pass


class MatcherError(BotError):
    """Raised when track matching fails."""
    pass


class DownloaderError(BotError):
    """Raised when downloading audio fails."""
    pass
