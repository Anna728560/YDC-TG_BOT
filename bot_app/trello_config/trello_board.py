import logging
import os
from typing import Any

import aiohttp
import requests
from dotenv import load_dotenv


load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
WEBHOOK = os.getenv("WEBHOOK")

logger = logging.getLogger()


async def check_board_exists() -> tuple[bool, Any] | tuple[bool, None]:
    """
    Checks if the Trello board
    named 'Trello_Tg_Bot_Board' exists for the authenticated user.

    :return: A tuple indicating whether the board exists
    and its ID if found, or None if not found.
    """
    url = "https://api.trello.com/1/members/me/boards"
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=query) as response:
            boards = await response.json()
            for board in boards:
                if board["name"] == "Trello_Tg_Bot_Board":
                    return True, board["id"]
    return False, None


async def create_board():
    """
    Creates a new Trello board named 'Trello_Tg_Bot_Board'.

    :return: The ID of the newly created Trello board.
    """
    url = "https://api.trello.com/1/boards/"
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "name": "Trello_Tg_Bot_Board",
        "defaultLists": "false"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=query) as response:
            board_id = (await response.json())["id"]
            return board_id


async def create_list(board_id, list_name):
    """
    Creates a new list on a Trello board.

    :param board_id: The ID of the Trello board where the list will be created.
    :param list_name: The name of the list to create.
    :return: The ID of the newly created Trello list.
    """
    url = f"https://api.trello.com/1/lists"
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "name": list_name,
        "idBoard": board_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=query) as response:
            return (await response.json())["id"]


async def setup_trello_board():
    """
    Sets up the Trello board for the Telegram bot.

    :return: None
    """
    board_exists, board_id = await check_board_exists()
    if not board_exists:
        board_id = await create_board()
        list_names = ["Done", "InProgress"]
        for name in list_names:
            await create_list(board_id, name)
        logger.info(f"Created board with id {board_id}; "
                    f"Columns: {', '.join(list_names)}")

    else:
        logger.info(f"Board already exists, skipping creation."
                    f"Bord id: {board_id}")

    return board_id

#     set_trello_webhook(board_id)
#
#
# def set_trello_webhook(board_id):
#     """
#     Sets up a webhook for Trello events on the specified board.
#
#     :param board_id: The ID of the Trello board to set up the webhook for.
#     :return: None
#     """
#     webhook = WEBHOOK + "/trello-webhook"
#     response = requests.request(
#         "POST",
#         f"https://api.trello.com/1/webhooks",
#         params={
#             "key": TRELLO_API_KEY,
#             "idModel": board_id,
#             "callbackURL": webhook,
#             "token": TRELLO_TOKEN,
#             "description": "Webhook"
#         }
#     )
#     if response.status_code == 200:
#         logger.info("Webhook created successfully")
#     else:
#         logger.info(f"Error creating webhook: {response.text} \n"
#                     f"key: {TRELLO_API_KEY} \n"
#                     f"idModel: {board_id} \n"
#                     f"callbackURL: {webhook} \n"
#                     f"token: {TRELLO_TOKEN} \n")
