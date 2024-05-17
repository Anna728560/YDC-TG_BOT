import logging
import sys
from aiohttp import web
from webhook_config.webhook_start import setup_webhook

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        app = setup_webhook()
        web.run_app(
            app,
            host="0.0.0.0",
            port=8002
        )
    except KeyboardInterrupt:
        print("Shutting down")
