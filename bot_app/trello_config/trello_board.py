import logging
import os
from typing import Tuple, Any

import aiohttp
import requests
from aiohttp import web
from dotenv import load_dotenv


load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
WEBHOOK = os.getenv("WEBHOOK")

logger = logging.getLogger()


async def check_board_exists() -> tuple[bool, Any] | tuple[bool, None]:
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

    handle_trello_webhook(board_id)


def handle_trello_webhook(board_id):
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
                    f"for board id: {board_id}")
