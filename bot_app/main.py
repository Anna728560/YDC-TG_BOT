import asyncio
import logging
import sys

from os import getenv
from dotenv import load_dotenv

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot_handlers import router
from database.db_config import setup_database


load_dotenv()
TOKEN = getenv("BOT_TOKEN")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(router)
    await bot.delete_webhook()
    await setup_database()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")