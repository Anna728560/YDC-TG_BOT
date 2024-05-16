import os
import asyncpg

from dotenv import load_dotenv


load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


async def set_user(username: str, user_id: int) -> None:
    """
    Adds a new user to the database_config
    if the user with the specified Username doesn't exist.

    Parameters:
        username (str): Username of the user.
        user_id (int): User ID of the user.

    Returns:
        None
    """
    try:
        connection = await asyncpg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

        await connection.execute(
            """
            INSERT INTO users (username, user_id)
            VALUES ($1, $2)
            ON CONFLICT (username) DO UPDATE
            SET username = EXCLUDED.username
            """,
            username, user_id
        )

    except Exception as _ex:
        print(f"[INFO] Error while connecting to PostgreSQL, {_ex}")