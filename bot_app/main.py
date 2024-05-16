import asyncio
import logging
import sys

from os import getenv
from dotenv import load_dotenv

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot_handlers import router
from database_config.db_config import setup_database
from trello_config.trello_board import setup_trello_board


load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")

logger = logging.getLogger()


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(router)
    await setup_database()
    await setup_trello_board()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down")
