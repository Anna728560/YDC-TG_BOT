import logging
import sys
from os import getenv

from aiohttp import web

from bot_app.database_config.db_config import setup_database
from bot_app.trello_config.trello_board import setup_trello_board
from bot_app.webhook_config.handlers import (
    handle_bot_webhook,
    accept_trello_webhook,
    handle_trello_webhook,
    set_bot_webhook,
    handle_get
)


app = web.Application()


async def on_startup(_):
    """
    Performs setup tasks when the application starts.

    This function is called when the application starts up.
    It is responsible for setting up the bot webhook,
    configuring the database, and initializing the Trello board.

    :return: None
    """
    await set_bot_webhook()
    await setup_database()
    await setup_trello_board()


def setup_webhook():
    """
    Sets up the webhook endpoints and registers the startup event handler.

    :return: The configured web application instance.
    """
    app.router.add_post("/trello-webhook", handle_trello_webhook)
    app.router.add_head("/trello-webhook", accept_trello_webhook)
    app.router.add_post(f"/{getenv("BOT_TOKEN")}", handle_bot_webhook)
    app.router.add_get("/", handle_get)
    app.on_startup.append(on_startup)
    return app


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        setup_webhook()
        web.run_app(
            app,
            host="0.0.0.0",
            port=3009
        )
    except KeyboardInterrupt:
        print("Shutting down")
