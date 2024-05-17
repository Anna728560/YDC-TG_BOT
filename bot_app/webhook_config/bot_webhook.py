from os import getenv

from aiohttp import web

from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot_app.bot_config.bot_handlers import router


BOT_WEBHOOK = getenv("BOT_WEBHOOK")
BOT_TOKEN = getenv("BOT_TOKEN")
WEBHOOK_URI = f"{BOT_WEBHOOK}/{BOT_TOKEN}"


dp = Dispatcher()
dp.include_router(router)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def set_bot_webhook():
    await bot.set_webhook(WEBHOOK_URI)


async def handle_bot_webhook(request):
    if request.content_type == "application/json":
        data = await request.json()
        token = request.path.split("/")[-1]
        if token == BOT_TOKEN:
            update = types.Update(**data)
            await dp.feed_update(bot, update)
            return web.Response(status=200)
    return web.Response(status=403)
