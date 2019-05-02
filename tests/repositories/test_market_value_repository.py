import pytest
import asynctest
from decimal import Decimal
from market_values_api.repositories.market_value_repository import MarketValueRepository

class TestMarketValueRepository(object):

    @pytest.fixture
    def mocked_client_class(self):
        with asynctest.patch(
            'market_values_api.repositories.clients.market_value_client.MarketValueClient',
            autospec=True, scope=asynctest.LIMITED
        ) as client_class:
            yield client_class

    @pytest.fixture
    def mock_client(self, mocked_client_class):
        def _mock_client_func(response_text='OK'):
            client = mocked_client_class.return_value
            client.get = asynctest.CoroutineMock(return_value=response_text)
            return client

        return _mock_client_func

    @pytest.fixture
    def mocked_parser_class(self):
        with asynctest.patch(
            'market_values_api.repositories.parsers.parse_market_value.ParseMarketValue',
            autospec=True, scope=asynctest.LIMITED
        ) as parser_class:
            yield parser_class

    @pytest.fixture
    def mock_parser(self, mocked_parser_class):
        def _mock_parser_func(market_value=Decimal('1')):
            parser = mocked_parser_class.return_value
            parser.call.return_value = market_value
            return parser

        return _mock_parser_func

    @pytest.mark.usefixtures("mocked_parser_class")
    async def test_call_instantiate_a_client_instance(self, session, mocked_client_class):
        await MarketValueRepository(session).get('CBA')
        mocked_client_class.assert_called_once_with(session)

    @pytest.mark.usefixtures("mocked_parser_class")
    async def test_call_uses_client_instance_to_get_raw_data(self, session, mock_client):
        client = mock_client()
        company_symbol = 'CBA'
        await MarketValueRepository(session).get(company_symbol)
        client.get.assert_awaited_once_with(company_symbol)

    async def test_call_instantiate_a_parser_instance(self, session, mock_client, mocked_parser_class):
        response_text = 'Dummy response text'
        mock_client(response_text)
        await MarketValueRepository(session).get('CBA')
        mocked_parser_class.assert_called_once_with(response_text)

    @pytest.mark.usefixtures("mocked_client_class")
    async def test_call_uses_parser_instance_to_parse_market_value(self, session, mock_parser):
        parser = mock_parser()
        await MarketValueRepository(session).get('CBA')
        parser.call.assert_called_once

    @pytest.mark.usefixtures("mocked_client_class")
    async def test_call_uses_parser_instance_to_parse_market_value(self, session, mock_parser):
        market_value = Decimal('1235.78')
        parser = mock_parser(market_value)
        company, market_value = await MarketValueRepository(session).get('CBA')
        assert (company, market_value) == ('CBA', market_value)
