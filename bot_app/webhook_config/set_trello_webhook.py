import logging
from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()


TRELLO_API_KEY = getenv("TRELLO_API_KEY")
WEBHOOK = getenv("WEBHOOK") + "/trello-webhook"
TRELLO_TOKEN = getenv("TRELLO_TOKEN")


logger = logging.getLogger()


def set_trello_webhook(board_id):
    """
    Sets up a webhook for Trello events on the specified board.

    :param board_id: The ID of the Trello board to set up the webhook for.
    :return: None
    """
    response = requests.request(
        "POST",
        f"https://api.trello.com/1/webhooks",
        params={
            "key": TRELLO_API_KEY,
            "idModel": board_id,
            "callbackURL": WEBHOOK,
            "token": TRELLO_TOKEN,
            "description": "Webhook"
        }
    )
    if response.status_code == 200:
        logger.info("Webhook created successfully")
    else:
        logger.info(f"Error creating webhook: {response.text} \n"
                    f"key: {TRELLO_API_KEY} \n"
                    f"idModel: {board_id} \n"
                    f"callbackURL: {WEBHOOK} \n"
                    f"token: {TRELLO_TOKEN} \n")
