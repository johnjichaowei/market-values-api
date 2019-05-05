import aiohttp
from market_values_api.handlers import MarketValuesHandler

def init_web_app():
    app = aiohttp.web.Application()
    app.on_startup.append(init_client_session)
    app.on_cleanup.append(close_client_session)
    setup_routes(app)
    return app

def setup_routes(app):
    app.router.add_get('/market_values', MarketValuesHandler().get)

async def init_client_session(app):
    app['client_session'] = aiohttp.ClientSession()

async def close_client_session(app):
    await app['client_session'].close()
