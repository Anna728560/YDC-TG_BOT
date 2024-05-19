from os import getenv
import logging
from aiohttp import web

from bot_app.database_config.db_config import setup_database
from bot_app.webhook_config.bot_webhook import (
    set_bot_webhook,
    handle_bot_webhook,
)
from bot_app.webhook_config.set_trello_webhook import (
    handle_trello_webhook,
    accept_trello_webhook
)


BOT_TOKEN = getenv("BOT_TOKEN")
GROUP_CHAT_ID = getenv("GROUP_CHAT_ID")

logger = logging.getLogger()
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


def setup_webhook():
    """
    Sets up the webhook endpoints and registers the startup event handler.
    :return: The configured web application instance.
    """
    app.router.add_post("/trello-webhook", handle_trello_webhook)
    app.router.add_head("/trello-webhook", accept_trello_webhook)
    app.router.add_post(f"/{BOT_TOKEN}", handle_bot_webhook)

    app.on_startup.append(on_startup)
    return app
