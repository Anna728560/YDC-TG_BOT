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
from bot_app.trello_config.trello_board import (
    get_in_progress_tasks_count,
    get_list_id
)


load_dotenv()
router = Router()

IN_PROGRESS_LIST_NAME = "InProgress"


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
    help_message = """
    Available commands:
    ⛳️ - /start: Start interacting with the bot
    🆘 - /help: Display available commands 
    🔖 - /progress: Show the number of tasks in the 'InProgress' column 
    """
    await message.answer(help_message)


@router.message(Command("progress"))
async def cmd_progress(message: Message):
    logger.info(f"Board ID: {config.BORD_ID}")
    if config.BORD_ID:
        list_id = await get_list_id(config.BORD_ID, IN_PROGRESS_LIST_NAME)
        if list_id:
            cards = await get_in_progress_tasks_count(list_id)
            if cards:
                card_list = "\n".join([f"- {card['name']}" for card in cards])
                await message.answer(
                    f"There are {len(cards)} tasks in the 'InProgress' column:\n{card_list}",
                    parse_mode=ParseMode.HTML
                )
            else:
                await message.answer("There are no tasks in the 'InProgress' column.")
