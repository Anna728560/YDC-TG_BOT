from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import bot_app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.username)
    await message.answer(
        "👋 Hello!"
    )
