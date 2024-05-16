import os

import aiohttp
import asyncio
from dotenv import load_dotenv


load_dotenv()

TRELLO_APY_KEY = os.getenv("TRELLO_APY_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")


async def check_board_exists() -> bool:
    url = "https://api.trello.com/1/members/me/boards"
    query = {
        "key": TRELLO_APY_KEY,
        "token": TRELLO_TOKEN,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=query) as response:
            boards = await response.json()
            for board in boards:
                if board["name"] == "Trello_Tg_Bot_Board":
                    return True
    return False


async def create_board():
    url = "https://api.trello.com/1/boards/"
    query = {
        "key": TRELLO_APY_KEY,
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
        "key": TRELLO_APY_KEY,
        "token": TRELLO_TOKEN,
        "name": list_name,
        "idBoard": board_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=query) as response:
            return (await response.json())["id"]


async def setup_trello_board():
    if not await check_board_exists():
        board_id = await create_board()
        list_names = ["Done", "InProgress"]
        for name in list_names:
            await create_list(board_id, name)
        print(f"Created board with id {board_id}; "
              f"columns: {', '.join(list_names)}")
    else:
        print("Board already exists, skipping creation.")


if __name__ == "__main__":
    asyncio.run(setup_trello_board())
