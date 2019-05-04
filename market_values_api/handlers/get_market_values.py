from aiohttp import web

async def get_market_values(request):
    session = request.app['client_session']
    return web.Response(text='Get market values!')
