from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from bot_app.database.models import Base


engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
