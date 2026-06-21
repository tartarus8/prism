from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Hi {html.bold(message.from_user.full_name)}! 🎧\n\n"
        "I am a modular, asynchronous Yandex Music downloader bot.\n"
        "Send me a Yandex Music track link, and I will:\n"
        "1. Extract its metadata\n"
        "2. Formulate a search query\n"
        "3. Simulate downloading the high-res FLAC\n"
        "4. Send the file back to you (within Telegram's 50MB bot upload limit)!\n\n"
        "Try sending a link like:\n"
        "<code>https://music.yandex.ru/album/1025555/track/9538356</code>"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🎧 Help & Info:\n\n"
        "Simply send a valid Yandex Music track link like:\n"
        "<code>https://music.yandex.ru/album/1025555/track/9538356</code>\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )
