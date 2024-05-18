import logging
from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()


TRELLO_API_KEY = getenv("TRELLO_API_KEY")
WEBHOOK = getenv("WEBHOOK") + "/trello-webhook"
TRELLO_TOKEN = getenv("TRELLO_TOKEN")


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
