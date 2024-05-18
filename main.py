import asyncio
import logging
import sys

import aiohttp
from aiohttp import web

from bot_app.trello_config.trello_board import setup_trello_board
from bot_app.webhook_config.set_trello_webhook import set_trello_webhook
from bot_app.webhook_config.webhook_start import setup_webhook


logger = logging.getLogger()


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app = setup_webhook()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=3009)
    await site.start()
    logger.info("Webhook server started")

    board_id = await setup_trello_board()
    logger.info(f"Board ID: {board_id}")

    async with aiohttp.ClientSession() as session:
        response = await set_trello_webhook(session, board_id)
        if response.status == 200:
            logger.info("Webhook created successfully")
        else:
            response_text = await response.text()
            logger.info(f"Error creating webhook: {response_text}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down")
    finally:
        loop.close()
