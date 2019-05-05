import pytest
from aiohttp import web
from market_values_api import init_web_app

@pytest.mark.usefixtures("session")
class TestWebApp(object):

    @pytest.fixture
    def cli(self, loop, aiohttp_client):
        app = init_web_app()
        return loop.run_until_complete(aiohttp_client(app))

    async def test_get_market_values_returns_400_when_companies_param_is_missed(self, cli):
        resp = await cli.get('/market_values')
        assert resp.status == 400
        response_text = await resp.text()
        assert 'The companies param is required' in response_text

    async def test_get_market_values_returns_response_in_json(self, cli, mock_response, make_raw_response_text):
        mock_response(response_text=make_raw_response_text('10.582B'))
        resp = await cli.get('/market_values?companies=REA')
        assert resp.status == 200
        response_text = await resp.text()
        assert response_text == '{"REA": 10582000000.000}'
