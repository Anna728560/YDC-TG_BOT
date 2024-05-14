from sqlalchemy import select

from bot_app.database.db_config import async_session
from bot_app.database.models import User


async def set_user(tg_id: int) -> None:
    """
    Adds a new user to the database
    if the user with the specified Telegram ID doesn't exist.

    Parameters:
        tg_id (int): Telegram ID of the user.

    Returns:
        None
    """
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
