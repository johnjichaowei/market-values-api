from aiohttp import web
from web_app import init_web_app

web.run_app(init_web_app(), port=80)
