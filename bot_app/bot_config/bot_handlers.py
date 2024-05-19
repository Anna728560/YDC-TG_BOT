import logging
import os

import aiohttp
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

from bot_app.database_config import db_requests as rq
from bot_app import config


load_dotenv()

router = Router()

IN_PROGRESS_LIST_NAME = "InProgress"
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
WEBHOOK = os.getenv("WEBHOOK")

logger = logging.getLogger()


@router.message(CommandStart())
async def cmd_start(message: Message):

    await rq.set_user(
        message.from_user.username,
        message.from_user.id,
        message.chat.id
    )
    await message.answer(
        f"👋 Hello, <b>{message.from_user.username}</b>!",
        parse_mode=ParseMode.HTML
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("help")


@router.message(Command("progress"))
async def cmd_progress(message: Message):
    logger.info(f"Board ID: {config.BORD_ID}")
    if config.BORD_ID:
        list_id = await get_list_id(config.BORD_ID, IN_PROGRESS_LIST_NAME)
        if list_id:
            task_count = await get_in_progress_tasks_count(list_id)
            await message.answer(f"There are {task_count} tasks in the 'InProgress' column.")
        else:
            await message.answer("Could not find the 'InProgress' column.")


async def get_in_progress_tasks_count(list_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.trello.com/1/lists/{list_id}/cards",
            params={
                "key": TRELLO_API_KEY,
                "token": TRELLO_TOKEN
            }
        ) as response:
            cards = await response.json()
            return len(cards)


async def get_list_id(board_id, list_name):
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
