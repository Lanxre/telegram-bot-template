import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_telegram_settings, load_database_settings
from utils import CommandList
from dispatcher import create_dispatcher
from logger import LoggerBuilder

logger = LoggerBuilder("TelegramBot").add_stream_handler().build()

telegram_settings = load_telegram_settings()
database_settings = load_database_settings()

async def on_startup(bot: Bot) -> None:
    logger.info("Starting up...")
    
    commands = CommandList()
    try:
        commands.load_from_json("./command_list.json")
        await bot.set_my_commands(commands=commands.get_commands())
        logger.info("Bot commands loaded and set")
    except Exception as e:
        logger.error(f"Failed to set commands: {e}")

async def on_shutdown(dispatcher: Dispatcher) -> None:
    logger.info("Shutting down...")
    
    db_manager = dispatcher.get("db_manager")
    if db_manager:
        await db_manager.connector.close()
        logger.info("Database connections closed")

async def main() -> None:
    dp = await create_dispatcher(database_settings)
    
    bot = Bot(
        token=telegram_settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")