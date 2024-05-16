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
WEB_HOOK_URL = getenv("WEB_HOOK_URL")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def on_startup(tg_bot: Bot) -> None:
    await tg_bot.set_webhook(f"{WEB_HOOK_URL}/webhook")


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    await setup_database()
    dp.startup.register(on_startup)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")
