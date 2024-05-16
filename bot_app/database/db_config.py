import asyncpg
import asyncio
import os

from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


async def setup_database() -> None:
    try:
        connection = await asyncpg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                user_id INT NOT NULL,
            )
            """
        )

    except Exception as _ex:
        print(f"[INFO] Error while connecting to PostgreSQL, {_ex}")


if __name__ == "__main__":
    asyncio.run(setup_database())
