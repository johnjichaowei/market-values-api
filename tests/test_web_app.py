import pytest
from aiohttp import web
from market_values_api import init_web_app

class TestWebApp(object):
    @pytest.fixture
    def cli(self, loop, aiohttp_client):
        app = init_web_app()
        return loop.run_until_complete(aiohttp_client(app))

    async def test_get_market_values(self, cli):
        resp = await cli.get('/market_values')
        assert resp.status == 200
        assert await resp.text() == 'Get market values!'
