import sys
from os import getenv
import logging
from aiohttp import web

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from bot_app.database_config.db_config import setup_database
from bot_app.trello_config.trello_board import setup_trello_board
from bot_app.webhook_config.bot_webhook import set_bot_webhook, handle_bot_webhook


BOT_TOKEN = getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
app = web.Application()


async def on_startup(_):
    await set_bot_webhook()
    await setup_database()
    await setup_trello_board()


async def handle_get(request):
    return web.Response(text="Hello, World!")


async def handle_trello_webhook(request):
    return web.Response(status=200)


def setup_webhook():
    app.router.add_get("/trello-webhook", handle_trello_webhook)
    app.router.add_post(f"/{BOT_TOKEN}", handle_bot_webhook)
    app.router.add_get("/", handle_get)
    app.on_startup.append(on_startup)
    return app
