import logging
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.exceptions import TelegramAPIError

from bot.core.exceptions import BotError
from bot.services.extractor_yandex import YandexMusicExtractor
from bot.services.matcher_heuristic import HeuristicMatcher
from bot.services.downloader_qobuz import QobuzDownloader
from bot.utils.helpers import get_file_size_mb, safe_delete_file
from bot.config import YANDEX_MUSIC_TOKEN, MOCK_FILE_SIZE_MB, DOWNLOAD_DIR

logger = logging.getLogger(__name__)
router = Router()

# Initialize services (strictly decoupled with defined configurations)
extractor = YandexMusicExtractor(token=YANDEX_MUSIC_TOKEN)
matcher = HeuristicMatcher()
downloader = QobuzDownloader(download_dir=DOWNLOAD_DIR, mock_file_size_mb=MOCK_FILE_SIZE_MB)


@router.message(F.text)
async def handle_music_link(message: Message):
    url = message.text.strip()
    
    # 1. Filter out messages that aren't Yandex Music URLs
    if not extractor.can_handle(url):
        # Offer a helpful hint if they sent an invalid music link
        if "music.yandex" in url:
            await message.reply(
                "❌ Invalid Yandex Music link format. It should look like:\n"
                "<code>https://music.yandex.ru/album/1025555/track/9538356</code>"
            )
        return

    status_message = await message.reply("🔍 Extracting track metadata from Yandex Music...")
    downloaded_file = None

    try:
        # 2. Extract Metadata from Yandex Music
        metadata = await extractor.extract_metadata(url)
        artists_str = ", ".join(metadata.artists)
        
        await status_message.edit_text(
            f"🎵 {artists_str} - {metadata.title}\n"
            f"💿 Album: {metadata.album or 'N/A'}\n"
            f"📅 Year: {metadata.release_year or 'N/A'}\n\n"
            "🎯 Matching track on high-res platform (Qobuz)..."
        )

        # 3. Match track via Heuristic matcher
        query = await matcher.match(metadata)

        await status_message.edit_text(
            f"🎵 {artists_str} - {metadata.title}\n"
            f"💿 Album: {metadata.album or 'N/A'}\n"
            f"📅 Year: {metadata.release_year or 'N/A'}\n\n"
            f"📥 Downloading high-res FLAC (mock size: {MOCK_FILE_SIZE_MB}MB)..."
        )

        # 4. Download file (mock delay of 3 seconds)
        downloaded_file = await downloader.download(query, metadata)

        # 5. Check file size against Telegram Bot limit (50MB)
        file_size = get_file_size_mb(downloaded_file)
        if file_size > 50.0:
            await status_message.edit_text(
                f"⚠️ File size is **{file_size:.2f}MB**, which exceeds Telegram's 50MB bot upload limit.\n\n"
                f"Track: {artists_str} - {metadata.title}\n"
                "Upload aborted."
            )
            return

        await status_message.edit_text("📤 Uploading FLAC audio to Telegram...")

        # Construct caption and details
        duration = int(metadata.duration_ms / 1000) if metadata.duration_ms else None
        caption = (
            f"🎧 {metadata.title}\n"
            f"👤 {artists_str}\n"
            f"💿 Album: {metadata.album or 'N/A'}\n"
            f"📅 Year: {metadata.release_year or 'N/A'}\n"
            f"📊 Size: {file_size:.2f} MB"
        )

        audio_file = FSInputFile(downloaded_file)
        
        # 6. Send the audio file to user
        await message.reply_audio(
            audio=audio_file,
            caption=caption,
            title=metadata.title,
            performer=artists_str,
            duration=duration
        )
        
        # Clean up the status message
        await status_message.delete()

    except BotError as e:
        logger.error(f"Bot error handling link: {e}")
        await status_message.edit_text(f"❌ Error: {str(e)}")
    except TelegramAPIError as e:
        logger.error(f"Telegram API error: {e}")
        await message.reply(f"❌ Telegram upload error: {str(e)}")
    except Exception as e:
        logger.exception("Unexpected error processing request")
        await status_message.edit_text(f"❌ An unexpected error occurred: {str(e)}")
    finally:
        # Guarantee cleanup of local file to prevent storage leakage
        if downloaded_file:
            safe_delete_file(downloaded_file)
