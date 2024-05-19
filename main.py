import asyncio
import logging
import sys

import aiohttp
from aiohttp import web

from bot_app.trello_config.trello_board import setup_trello_board
from bot_app.webhook_config.set_trello_webhook import set_trello_webhook
from bot_app.webhook_config.webhook_start import setup_webhook
from bot_app import config

logger = logging.getLogger()


async def main():
    """
    Sets up and runs the webhook server, configures the Trello board,
    and sets up a webhook for Trello events.

    This function performs the following steps:
    1. Configures logging to output to stdout.
    2. Sets up and starts an aiohttp web server to handle webhook events.
    3. Configures a Trello board by creating it if it doesn't exist, or retrieving its ID if it does.
    4. Sets up a webhook on the Trello board to capture events and send them to the configured URL.

    :return: None
    """

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app = setup_webhook()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=3009)
    await site.start()
    logger.info("Webhook server started")

    # board_id = await setup_trello_board()
    # config.BORD_ID = board_id
    # logger.info(f"Set global BORD_ID to {config.BORD_ID}")
    try:
        board_id = await setup_trello_board()
        config.BORD_ID = board_id
        logger.info(f"Set global BORD_ID to {config.BORD_ID}")
    except Exception as ex_:
        logger.info(f"Board already exists, skipping creation. Board ID: {config.BORD_ID}")

    async with aiohttp.ClientSession() as session:
        response = await set_trello_webhook(session, config.BORD_ID)
        if response.status == 200:
            logger.info("Webhook created successfully")
        else:
            response_text = await response.read()
            logger.info(f"Error creating webhook: {response_text.decode()}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down")
    finally:
        loop.close()
