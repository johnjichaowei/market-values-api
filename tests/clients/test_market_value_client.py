import aiohttp
import pytest
import asynctest
from market_values_api.clients import MarketValueClient
from market_values_api.exceptions import MarketValueClientError

class TestMarketValueClient(object):

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
