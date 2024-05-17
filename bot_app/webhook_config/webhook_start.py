import json
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
from bot_app.webhook_config.bot_webhook import CHAT_ID


BOT_TOKEN = getenv("BOT_TOKEN")

logger = logging.getLogger()

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
    try:
        logger.info(f"Received Trello webhook request: {request.method} {request.path}")

        data = await request.json()
        logger.info(f"Received Trello webhook: {json.dumps(data, indent=2)}")

        action_type = data["action"]["type"]
        card_name = data["action"]["data"]["card"]["name"]
        board_name = data["action"]["data"]["board"]["name"]

        list_before = data["action"]["data"].get("listBefore", {}).get("name", "")
        list_after = data["action"]["data"].get("listAfter", {}).get("name", "")

        member_creator = data["action"]["memberCreator"]["fullName"]

        message = (f"***<b>New action on Trello</b>***\n\n"
                   f"<b>Type:</b> {action_type}\n"
                   f"<b>Card:</b> {card_name}\n"
                   f"<b>Board:</b> {board_name}\n"
                   f"<b>By:</b> {member_creator}\n")

        if list_before and list_after:
            message += f"<b>Moved from 📥</b> {list_before} <b>to</b> 📤 {list_after}\n"
        elif list_before:
            message += f"<b>Previous list 📥:</b> {list_before}\n"
        elif list_after:
            message += f"<b>New list 📤:</b> {list_after}\n"

        await bot.send_message(chat_id=467362391, text=message, parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(f"Error handling Trello webhook: {e}")

    return web.Response(status=200)


async def accept_trello_webhook(request):
    return web.Response(text="OK")


def setup_webhook():
    app.router.add_post("/trello-webhook", handle_trello_webhook)
    app.router.add_head("/trello-webhook", accept_trello_webhook)
    app.router.add_post(f"/{BOT_TOKEN}", handle_bot_webhook)

    app.on_startup.append(on_startup)
    return app
