import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from database_config import db_requests as rq

router = Router()
logger = logging.getLogger('example_logger')


@router.message(CommandStart())
async def cmd_start(message: Message):

    await rq.set_user(
        message.from_user.username,
        message.from_user.id
    )

    logger.warning('This is a warning')
    logger.info("Here is message", message.from_user.username, message.from_user)

    await message.answer(
        f"👋 Hello, <b>{message.from_user.username}</b>!",
        parse_mode=ParseMode.HTML
    )
