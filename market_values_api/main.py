import logging
from aiohttp import web
from web_app import init_web_app

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

web.run_app(init_web_app(), port=80)
