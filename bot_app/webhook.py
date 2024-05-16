import asyncio
import logging
import sys

from os import getenv

from aiohttp import web
from dotenv import load_dotenv

from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot_handlers import router
from database_config.db_config import setup_database
from trello_config.trello_board import setup_trello_board


load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
NGROK = getenv("NGROK")
URL = f"{TELEGRAM_API_URL}/setWebhook?url={NGROK}/webhook"

dp = Dispatcher()
dp.include_router(router)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

app = web.Application()


async def set_webhook():
    webhook_uri = f"{NGROK}/{BOT_TOKEN}"
    await bot.set_webhook(webhook_uri)


async def on_shutdown(_):
    await bot.delete_webhook()


async def on_startup(_):
    await set_webhook()
    await setup_database()
    await setup_trello_board()


async def handle_webhook(request):
    if request.content_type == "application/json":
        data = await request.json()
        token = request.path.split("/")[-1]
        if token == BOT_TOKEN:
            update = types.Update(**data)
            await dp.feed_update(bot, update)
            return web.Response(status=200)
    return web.Response(status=403)


app.router.add_post(f"/{BOT_TOKEN}", handle_webhook)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        app.on_shutdown.append(on_shutdown)
        app.on_startup.append(on_startup)
        web.run_app(
            app,
            host="0.0.0.0",
            port=8000
        )
    except KeyboardInterrupt:
        print("Shutting down")
