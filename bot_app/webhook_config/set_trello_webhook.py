import json
import logging
from os import getenv

import aiohttp
from aiogram.enums import ParseMode
from aiohttp import web
from dotenv import load_dotenv

from bot_app.webhook_config.bot_webhook import bot


load_dotenv()


TRELLO_API_KEY = getenv("TRELLO_API_KEY")
WEBHOOK = getenv("WEBHOOK") + "/trello-webhook"
TRELLO_TOKEN = getenv("TRELLO_TOKEN")
GROUP_CHAT_ID = getenv("GROUP_CHAT_ID")


logger = logging.getLogger()


async def set_trello_webhook(session, board_id):
    """
    Sets up a webhook for Trello events on the specified board.

    :param session: The aiohttp client session.
    :param board_id: The ID of the Trello board to set up the webhook for.
    :return: The response of the webhook setup request.
    """
    async with session.post(
        f"https://api.trello.com/1/webhooks",
        params={
            "key": TRELLO_API_KEY,
            "idModel": board_id,
            "callbackURL": WEBHOOK,
            "token": TRELLO_TOKEN,
            "description": "Webhook"
        }
    ) as response:
        return response


async def accept_trello_webhook(request):
    """
    Accepts the Trello webhook request and returns an OK response.

    :param request: The incoming request from Trello webhook.
    :return: A response indicating the acceptance of the request.
    """
    return web.Response(status=200)


async def handle_trello_webhook(request):
    """
    Handles incoming Trello webhook requests.

    :param request: The incoming request from Trello webhook.
    :return: A response indicating the status of the request.
    """
    try:
        logger.info(f"Received Trello webhook request: {request.method} {request.path}")

        data = await request.json()
        logger.info(f"Received Trello webhook: {json.dumps(data.get('action', {}), indent=2)}")

        action_type = data["action"]["type"]
        card_name = data["action"]["data"]["card"]["name"]
        board_name = data["action"]["data"]["board"]["name"]

        list_before = data["action"]["data"].get("listBefore", {}).get("name", "")
        list_after = data["action"]["data"].get("listAfter", {}).get("name", "")

        member_creator = data["action"]["memberCreator"]["fullName"]

        message = (f"***<b>New action on Trello</b>***\n\n"
                   f"<code>TYPE:  {action_type}\n"
                   f"CARD:  {card_name}\n"
                   f"BOARD: {board_name}\n"
                   f"BY:    {member_creator}\n\n</code>")

        if list_before and list_after:
            message += f"<code>FROM: {list_before}\nTO: {list_after}\n</code>"
        elif list_before:
            message += f"<code>Previous list : {list_before}\n</code>"
        elif list_after:
            message += f"<code>New list : {list_after}\n</code>"

        async with aiohttp.ClientSession() as session:
            await bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=message,
                parse_mode=ParseMode.HTML
            )

    except Exception as e:
        logger.error(f"Error handling Trello webhook: {e}")

    return web.Response(status=200)

