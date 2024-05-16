import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot_app.database_config import db_requests as rq

router = Router()
loger = logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@router.message(CommandStart())
async def cmd_start(message: Message):

    await rq.set_user(
        message.from_user.username,
        message.from_user.id
    )
    loger.info(message.from_user.username)
    await message.answer(
        f"👋 Hello, <b>{message.from_user.username}</b>!",
        parse_mode=ParseMode.HTML
    )
