from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot_app.database import db_requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.username)
    await message.answer(
        "👋 Hello!"
    )
