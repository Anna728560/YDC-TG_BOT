import json
from os import getenv
import logging

import aiohttp
from aiohttp import web
from aiogram.enums import ParseMode

from bot_app.database_config.db_config import setup_database
from bot_app.webhook_config.bot_webhook import (
    set_bot_webhook,
    handle_bot_webhook,
)
from bot_app.webhook_config.set_trello_webhook import (
    handle_trello_webhook,
    accept_trello_webhook
)

BOT_TOKEN = getenv("BOT_TOKEN")
GROUP_CHAT_ID = getenv("GROUP_CHAT_ID")

logger = logging.getLogger()
app = web.Application()


async def on_startup(_):
    """
    Performs setup tasks when the application starts.

    This function is called when the application starts up.
    It is responsible for setting up the bot webhook,
    configuring the database, and initializing the Trello board.

    :return: None
    """
    await set_bot_webhook()
    await setup_database()


# async def handle_trello_webhook(request):
#     """
#     Handles incoming Trello webhook requests.
#
#     :param request: The incoming request from Trello webhook.
#     :return: A response indicating the status of the request.
#     """
#     try:
#         logger.info(f"Received Trello webhook request: {request.method} {request.path}")
#
#         data = await request.json()
#         logger.info(f"Received Trello webhook: {json.dumps(data, indent=2)}")
#
#         action_type = data["action"]["type"]
#         card_name = data["action"]["data"]["card"]["name"]
#         board_name = data["action"]["data"]["board"]["name"]
#
#         list_before = data["action"]["data"].get("listBefore", {}).get("name", "")
#         list_after = data["action"]["data"].get("listAfter", {}).get("name", "")
#
#         member_creator = data["action"]["memberCreator"]["fullName"]
#
#         message = (f"***<b>New action on Trello</b>***\n\n"
#                    f"<b>Type:</b>  {action_type}\n"
#                    f"<b>Card:</b>  {card_name}\n"
#                    f"<b>Board:</b> {board_name}\n"
#                    f"<b>By:</b>    {member_creator}\n\n")
#
#         if list_before and list_after:
#             message += f"<b>FROM:</b> {list_before}\n<b>TO:</b> {list_after}\n"
#         elif list_before:
#             message += f"<b>Previous list :</b> {list_before}\n"
#         elif list_after:
#             message += f"<b>New list :</b> {list_after}\n"
#
#         async with aiohttp.ClientSession() as session:
#             await bot.send_message(
#                 chat_id=GROUP_CHAT_ID,
#                 text=message,
#                 parse_mode=ParseMode.HTML
#             )
#
#     except Exception as e:
#         logger.error(f"Error handling Trello webhook: {e}")
#
#     return web.Response(status=200)
#
#
# async def accept_trello_webhook(request):
#     """
#     Accepts the Trello webhook request and returns an OK response.
#
#     :param request: The incoming request from Trello webhook.
#     :return: A response indicating the acceptance of the request.
#     """
#     return web.Response(status=200)


def setup_webhook():
    """
    Sets up the webhook endpoints and registers the startup event handler.
    :return: The configured web application instance.
    """
    app.router.add_post("/trello-webhook", handle_trello_webhook)
    app.router.add_head("/trello-webhook", accept_trello_webhook)
    app.router.add_post(f"/{BOT_TOKEN}", handle_bot_webhook)

    app.on_startup.append(on_startup)
    return app
