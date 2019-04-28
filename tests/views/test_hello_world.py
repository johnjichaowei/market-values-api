import pytest
from aiohttp import web
from market_values_api.views import hello_world

class TestHelloWorld(object):
    async def test_index(self, cli):
        resp = await cli.get('/')
        assert resp.status == 200
        assert await resp.text() == 'Hello Aiohttp!'

    @pytest.fixture
    def cli(self, loop, aiohttp_client):
        app = web.Application()
        app.router.add_get('/', hello_world.index)
        return loop.run_until_complete(aiohttp_client(app))
