import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_telegram_settings, load_database_settings
from utils import CommandList
from dispatcher import create_dispatcher
from logger import LoggerBuilder

logger = LoggerBuilder("TelegramBot").add_stream_handler().build()

telegram_settings = load_telegram_settings()
database_settings = load_database_settings()

async def main() -> None:
    dp = await create_dispatcher(database_settings.name)
    bot = Bot(
        token=telegram_settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Set commands
    commands = CommandList()
    commands.load_from_json("./command_list.json")
    await bot.set_my_commands(commands=commands.get_commands())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Bot start")
    asyncio.run(main())
    logger.info("Bot stoped")