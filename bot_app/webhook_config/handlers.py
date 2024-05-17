import json
import logging
from os import getenv

from aiohttp import web

from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot_app.bot_config.bot_handlers import router


CHAT_ID = None

WEBHOOK = getenv("WEBHOOK")
BOT_TOKEN = getenv("BOT_TOKEN")
WEBHOOK_URI = f"{WEBHOOK}/{BOT_TOKEN}"

logger = logging.getLogger()

dp = Dispatcher()
dp.include_router(router)
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def set_bot_webhook():
    await bot.set_webhook(WEBHOOK_URI)


async def handle_bot_webhook(request):
    """
    Handles incoming webhook requests from the Telegram bot.

    :param request: The incoming request object.
    :return: A web response with a status code
    indicating the result of the request processing.
    """
    global CHAT_ID
    if request.content_type == "application/json":
        data = await request.json()
        token = request.path.split("/")[-1]

        if token == BOT_TOKEN:
            update = types.Update(**data)
            CHAT_ID = update.message.chat.id
            logger.info(f"Set chat id: {CHAT_ID}")
            await dp.feed_update(bot, update)
            return web.Response(status=200)

    return web.Response(status=403)


async def handle_get(request):
    """
    Request handler for GET requests.
    """
    return web.Response(text="Hello, World!")


async def handle_trello_webhook(request):
    """
    Handles incoming Trello webhook requests.

    :param request: The incoming request from Trello webhook.
    :return: A response indicating the status of the request.
    """
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
                   f"<b>Type:</b>  {action_type}\n"
                   f"<b>Card:</b>  {card_name}\n"
                   f"<b>Board:</b> {board_name}\n"
                   f"<b>By:</b>    {member_creator}\n\n")

        if list_before and list_after:
            message += f"<b>FROM:</b> {list_before}\n<b>TO:</b> {list_after}\n"
        elif list_before:
            message += f"<b>Previous list :</b> {list_before}\n"
        elif list_after:
            message += f"<b>New list :</b> {list_after}\n"

        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(f"Error handling Trello webhook: {e}")

    return web.Response(status=200)


async def accept_trello_webhook(request):
    """
    Accepts the Trello webhook request and returns an OK response.

    :param request: The incoming request from Trello webhook.
    :return: A response indicating the acceptance of the request.
    """
    return web.Response(text="OK")
