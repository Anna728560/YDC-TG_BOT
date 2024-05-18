import logging
import sys
from aiohttp import web

from bot_app.trello_config.trello_board import setup_trello_board
from bot_app.webhook_config.set_trello_webhook import set_trello_webhook
from bot_app.webhook_config.webhook_start import setup_webhook


logger = logging.getLogger()

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        app = setup_webhook()
        web.run_app(
            app,
            host="0.0.0.0",
            port=3009
        )
        bord_id = setup_trello_board()
        logger.info(f"Board ID: {bord_id}")
        response = set_trello_webhook(bord_id)
        if response.status_code == 200:
            logger.info("Webhook created successfully")
        else:
            logger.info(f"Error creating webhook: {response.text} \n")

    except KeyboardInterrupt:
        print("Shutting down")
