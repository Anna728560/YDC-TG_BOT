import logging
import os
from typing import Any

import aiohttp
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


async def get_in_progress_tasks_count(list_id):
    """
    Retrieves the tasks in the specified Trello list.

    :param list_id: The ID of the Trello list to fetch tasks from.
    :type list_id: str
    :return: A list of tasks in the specified list.
    :rtype: list
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.trello.com/1/lists/{list_id}/cards",
            params={
                "key": TRELLO_API_KEY,
                "token": TRELLO_TOKEN
            }
        ) as response:
            cards = await response.json()
            return cards


async def get_list_id(board_id, list_name):
    """
    Retrieves the ID of a Trello list with the specified name from a given board.

    :param board_id: The ID of the Trello board to search for the list.
    :type board_id: str
    :param list_name: The name of the Trello list to find.
    :type list_name: str
    :return: The ID of the list if found, otherwise None.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.trello.com/1/boards/{board_id}/lists",
            params={
                "key": TRELLO_API_KEY,
                "token": TRELLO_TOKEN
            }
        ) as response:
            lists = await response.json()
            for lst in lists:
                if lst["name"] == list_name:
                    return lst["id"]
            return None
