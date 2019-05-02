import aiohttp
import pytest
import asynctest
import os
from market_values_api.repositories.clients.market_value_client import MarketValueClient
from market_values_api.exceptions.market_value_client_error import MarketValueClientError

class TestMarketValueClient(object):

    @pytest.fixture
    def host_url(self):
        return 'http://dummy-url'

    @pytest.fixture
    def set_url_env(self, host_url):
        with asynctest.patch.dict(os.environ, {'MARKET_VALUE_HOST_URL': host_url}, scope=asynctest.LIMITED) as patched_env:
            yield patched_env

    @pytest.fixture
    def mock_response(self, session):
        def _mock_response_func(response_code=200, response_text='OK'):
            with asynctest.patch('aiohttp.ClientResponse', autospec=True, scope=asynctest.LIMITED) as resp_class:
                response = resp_class.return_value
                response.status = response_code
                response.text = asynctest.CoroutineMock(return_value=response_text)
                response.__aenter__.return_value = response
                session.get.return_value = response

        return _mock_response_func

    @pytest.mark.usefixtures("set_url_env")
    async def test_get_calls_get_method_of_session_client(self, host_url, session, mock_response):
        mock_response()
        company_symbol = 'CBA'
        client = MarketValueClient(session)
        result = await client.get(company_symbol)
        session.get.assert_called_once_with(f"{host_url}/quote/{company_symbol}.AX")

    @pytest.mark.usefixtures("set_url_env")
    async def test_get_returns_response_text(self, session, mock_response):
        response_text = 'Dummy response text'
        mock_response(response_text=response_text)
        client = MarketValueClient(session)
        result = await client.get('CBA')
        assert result == response_text

    @pytest.mark.usefixtures("set_url_env")
    async def test_get_raises_exception_if_not_200(self, session, mock_response):
        response_code = 400
        mock_response(response_code)
        client = MarketValueClient(session)
        with pytest.raises(MarketValueClientError) as err:
            await client.get('CBA')
        assert f"Failed to get market value for client, resposne code {response_code}" in str(err)
