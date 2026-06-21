import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.config import BOT_TOKEN
from bot.handlers import start, music

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    """Register commands to show up in Telegram's menu."""
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help information"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    if not BOT_TOKEN:
        logger.critical(
            "BOT_TOKEN is not set in the environment or .env file!\n"
            "Please create a .env file and set BOT_TOKEN=<your_token_here>"
        )
        sys.exit("Error: BOT_TOKEN is missing.")

    # Initialize bot with HTML parse mode as default
    try:
        from aiogram.client.default import DefaultBotProperties
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    except ImportError:
        # Compatibility fallback for older aiogram v3 versions
        bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()

    # Register routers (order is important: command handlers first, then text matching)
    dp.include_router(start.router)
    dp.include_router(music.router)

    # Register menu commands
    await set_commands(bot)

    logger.info("Starting Telegram Bot polling...")
    try:
        # Clear webhook before starting polling to prevent conflict errors
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped gracefully.")
